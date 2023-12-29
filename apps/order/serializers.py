from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from jenkins import JenkinsException, Jenkins
from utils.devops_api_log import logger
from apps.order.models import *
from apps.config.serializers import ServiceEnvironmentSerializer
from apps.account.serializers import UserSerializer
from apps.config.models import Jenkins as jenkins_models


def get_next_build_number(jks: Jenkins):
    """
    :return: number
    """
    from django.db.models import Max
    print(jks)
    jk = Jenkins(
        jks.address,
        username='yaoshaoqiang',
        password='w9vM7BQoED6fg.uheO'
    )
    model_id = JenkinsOrders.objects.all().aggregate(Max('jenkins_order_id'))
    jk_data = jk.get_job_info(jks.name)
    jk_next_id = int(jk_data['nextBuildNumber'])
    model_next_id = int(model_id['jenkins_order_id__max']) + 1
    if jk_next_id > model_next_id:
        return jk_next_id
    else:
        return model_next_id


class JenkinsLogField(serializers.Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value: JenkinsOrders):
        # jks = Jenkins(
        #     value.jenkins.address,
        #     username='yaoshaoqiang',
        #     password='w9vM7BQoED6fg.uheO'
        # )
        try:
            logger.info('获取：{}，日志'.format(value.jenkins_order_id))
            # data = jks.get_build_console_output(
            #     name=value.jenkins.name,
            #     number=value.jenkins_order_id
            # )
            logger.info("获取到的Jenkins:{}".format(value.output))
            return "<div>{}</div>".format(value.output.replace('\n', '</br>'))
        except Exception as e:
            logger.error(msg="未获取到相关日志:{}".format(e))
            return "未获取到相关日志"


class JenkinsOrdersSerializer(serializers.ModelSerializer):
    jenkins_address = serializers.CharField(source='jenkins.address', read_only=True)
    service_environment = ServiceEnvironmentSerializer(source='service_env', read_only=True)
    jenkins_log = JenkinsLogField(read_only=True)
    order_user = UserSerializer(read_only=True)

    class Meta:
        model = JenkinsOrders
        fields = "__all__"

    def validate(self, data):
        order_user = self.context['request'].user
        data['order_user'] = order_user
        return data

    def create(self, validated_data):
        next_number = get_next_build_number(jks=validated_data['jenkins'])
        validated_data['jenkins_order_id'] = next_number
        logger.info("下一个任务id为:{}".format(next_number))
        instance = JenkinsOrders.objects.create(**validated_data)
        instance.save()
        return instance


class SubOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubOrders
        fields = "__all__"


class OrderLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLogs
        fields = "__all__"


class OrdersSerializer(serializers.ModelSerializer):
    suborders = SubOrderSerializer(many=True)
    order_logs = OrderLogsSerializer(many=True, read_only=True)
    status = serializers.IntegerField(read_only=True)
    finish_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Orders
        # fields = ('suborders', 'order_time', 'notice', 'desc', 'id')
        fields = '__all__'

    def create(self, validated_data):
        suborders = validated_data.pop('suborders')
        notice = validated_data.pop('notice')
        validated_data['status'] = 0
        instance = Orders.objects.create(**validated_data)
        instance.notice.set(notice)
        for suborder in suborders:
            suborder['order'] = instance
            SubOrders.objects.create(**suborder)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        suborders_data = validated_data.pop('suborders')
        notice = validated_data.pop('notice')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.notice.set(notice)
        instance.save()
        SubOrders.objects.filter(order=instance).delete()
        for suborder in suborders_data:
            suborder['order'] = instance
            SubOrders.objects.create(**suborder)
        return instance


class ContentTypeField(serializers.Field):
    def get_attribute(self, instance):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return instance

    def to_representation(self, value: ContentType):
        """
        Serialize the value's class name.
        """
        from apps.config import serializers
        model_class = value.model_class()
        model_serializer_name = "{}Serializer".format(model_class.__name__)
        model_serializer = getattr(serializers, model_serializer_name)
        mode_info = value.natural_key()
        data = dict()
        if mode_info[1] not in ['db', 'nacos', 'kuberneteshelmchartmodel']:
            raise ValueError(_("Invalid value"))
        model_data = model_serializer(instance=model_class.objects.all(), many=True)
        data['label'] = mode_info[1]
        data['child'] = model_data.data
        return data


class ContentTypeSerializer(serializers.ModelSerializer):
    model = ContentTypeField()

    class Meta:
        model = ContentType
        fields = "__all__"


__all__ = [
    'OrdersSerializer',
    'SubOrderSerializer',
    'ContentTypeSerializer',
    'JenkinsOrdersSerializer'
]

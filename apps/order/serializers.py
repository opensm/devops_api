from rest_framework import serializers
from apps.order.models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType


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
    'ContentTypeSerializer'
]

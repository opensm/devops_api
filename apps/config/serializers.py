from rest_framework import serializers
from apps.config.models import *
from django.utils.translation import gettext_lazy as _
from apps.jira.models import JiraProjectVersion
from utils.devops_api_log import logger
from django.contrib.contenttypes.models import ContentType


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ("app_label", "model", "id")


class EnvironmentFields(serializers.RelatedField):
    def get_attribute(self, instance):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return instance

    def to_representation(self, value: Environment):
        content_object_list = list()
        content_object_data_dict = dict()
        for content in ContentType.objects.filter(
                app_label='config',
                model__in=['nacos', 'db', 'serviceenvironment']
        ):
            if content.model in ['nacos']:
                append_args = ['address', 'id', 'namespace', 'project__name', 'environment__environment']
            elif content.model in ['db']:
                append_args = ['address', 'db_type', 'id', 'project__name', 'environment__environment']
            else:
                append_args = ['service__service_name', 'id', 'project__name', 'environment__environment']

            content_object_list.append({
                'value': content.id,
                'label': "{}-{}".format(
                    content.app_label,
                    content.model
                ),
                'name': content.model
            })
            # content_object_data_dict[content.id] = content.get_all_objects_for_this_type(
            #     environment=value
            # ).values(
            #     *append_args
            # )
            extra_data = list()
            for extra in content.get_all_objects_for_this_type(
                    environment=value
            ).values(
                *append_args
            ):
                if 'service__service_name' in extra.keys():
                    extra_data.append({
                        'label': '项目：{project__name}，环境：{environment__environment}，服务名：{service__service_name}'.format(
                            **extra
                        ),
                        'value': '{id}'.format(**extra)
                    })
                elif 'namespace' in extra.keys():
                    extra_data.append({
                        'label': '项目：{project__name}，环境：{environment__environment}，命名空间：{namespace}，地址：{address}'.format(
                            **extra
                        ),
                        'value': '{id}'.format(**extra)
                    })
                elif 'db_type' in extra.keys():
                    extra_data.append({
                        'label': '项目：{project__name}，环境：{environment__environment}，数据库类型：{db_type}，地址：{address}'.format(
                            **extra
                        ),
                        'value': '{id}'.format(**extra)
                    })
                else:
                    logger.warning("未知配置类型")
            content_object_data_dict[content.id] = extra_data

        return {'content': content_object_list, 'objects': content_object_data_dict}


class ProjectsSerializer(serializers.ModelSerializer):
    harbor_password = serializers.CharField(write_only=True)
    git_token = serializers.CharField(write_only=True)

    class Meta:
        model = Projects
        fields = "__all__"

    def validate(self, attrs):
        from utils.core.rsa_crypt import generator
        attrs['harbor_password'] = generator.decrypt_data(data=attrs['harbor_password'])
        attrs['git_token'] = generator.decrypt_data(data=attrs['git_token'])
        return attrs


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"


class EnvironmentSerializer(serializers.ModelSerializer):
    children = EnvironmentFields(read_only=True)
    label = serializers.CharField(read_only=True, source="environment")
    value = serializers.CharField(read_only=True, source="id")

    class Meta:
        model = Environment
        fields = "__all__"


class KubernetesModelSerializer(serializers.ModelSerializer):
    kubeconfig = serializers.CharField(write_only=True)

    class Meta:
        model = KubernetesModel
        fields = "__all__"


class SSHKeySerializer(serializers.ModelSerializer):
    ssh_password = serializers.CharField(write_only=True)
    ssh_public_key = serializers.CharField(write_only=True)

    class Meta:
        model = SSHKey
        fields = "__all__"

    def validate(self, attrs):
        from utils.core.rsa_crypt import generator
        attrs['ssh_password'] = generator.decrypt_data(data=attrs['ssh_password'])
        attrs['ssh_public_key'] = generator.decrypt_data(data=attrs['ssh_public_key'])
        return attrs


class ServiceConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceConfig
        fields = "__all__"


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"


class ServiceResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceResource
        fields = "__all__"


class KubernetesEnvironmentConfigurationSerializer(serializers.ModelSerializer):
    rw_kubernetes_auth = serializers.CharField(source='kubernetes_auth.name', read_only=True)

    class Meta:
        model = KubernetesEnvironmentConfiguration
        fields = "__all__"


class DockerEnvironmentConfigurationSerializer(serializers.ModelSerializer):
    rw_docker_ssh = serializers.CharField(source='docker_ssh.ssh_name', read_only=True)

    class Meta:
        model = DockerEnvironmentConfiguration
        fields = "__all__"


class ServiceEnvironmentFields(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Environment):
            return value.environment
        elif isinstance(value, Services):
            return value.service_name
        elif isinstance(value, ServiceResource):
            return "<span>需求CPU:{},内存:{}<br/>限制CPU:{},内存:{}<span>".format(
                value.request_cpu,
                value.request_memory,
                value.limit_cpu,
                value.limit_memory
            )
        elif isinstance(value, ServiceConfig):
            print(value)
            for x in value.all():
                print(x)
            return '<br/>'.join(x)
        elif isinstance(value, KubernetesEnvironmentConfiguration):
            return value.kubernetes_namespace
        elif isinstance(value, DockerEnvironmentConfiguration):
            return value.docker_instances
        elif isinstance(value, Projects):
            return value.name
        else:
            return "无"


class ProductField(serializers.Field):
    def get_attribute(self, instance):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return instance

    def to_representation(self, value: ServiceEnvironment):
        """
        Serialize the value's class name.
        """
        products = Products.objects.filter(service=value.service)
        data = ProductsSerializer(instance=products, many=True)
        return data.data


class ServiceEnvironmentSerializer(serializers.ModelSerializer):
    # detail = ServiceEnvironmentFields()
    rw_environment = ServiceEnvironmentFields(source="environment", read_only=True)
    rw_service = ServiceEnvironmentFields(source='service', read_only=True)
    rw_resource = ServiceEnvironmentFields(source='resource', read_only=True)
    # rw_service_config = ServiceEnvironmentFields(source='service_config', read_only=True)
    rw_kubernetes_environment_config = ServiceEnvironmentFields(source='kubernetes_environment_config', read_only=True)
    rw_docker_environment_config = ServiceEnvironmentFields(source='docker_environment_config', read_only=True)
    rw_project = ServiceEnvironmentFields(source='project', read_only=True)
    production = ProductField(read_only=True)

    class Meta:
        model = ServiceEnvironment
        fields = "__all__"


class KubernetesHelmRepoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesHelmRepoModel
        fields = "__all__"


class KubernetesHelmChartModelSerializer(serializers.ModelSerializer):
    rw_helm_repo = serializers.CharField(source="helm_repo.name", read_only=True)

    class Meta:
        model = KubernetesHelmChartModel
        fields = "__all__"


class EnvironmentVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentVariable
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    rw_service_environment = ServiceEnvironmentSerializer(many=True, source="service_environment", read_only=True)
    rw_service = serializers.SlugRelatedField(source="service", slug_field='service_name', read_only=True)

    class Meta:
        model = Products
        fields = "__all__"

    def validate(self, attrs):
        images = attrs['images']
        try:
            self.get_image_version(images)
        except Exception as e:
            raise serializers.ValidationError("没有正确匹配镜像格式，无法找到对应版本号：".format(e))
        return attrs

    def get_image_version(self, images):
        import re
        pattern = re.compile("(.*):(\d{14})-(.*)-([0-9a-z]{6})")
        result2 = pattern.match(images)
        version = result2.groups()[2]
        return version

    def create(self, validated_data):
        version = self.get_image_version(validated_data['images'])
        service_environment = None
        try:
            jira = JiraProjectVersion.objects.get(name=version)
            validated_data['jira_version'] = jira.id
        except JiraProjectVersion.DoesNotExist:
            logger.error("没有关联到 jira版本")
        if 'service_environment' in validated_data.keys():
            service_environment = validated_data.pop('service_environment')
        instance = Products.objects.create(**validated_data)
        if service_environment:
            instance.service_environment.set(service_environment)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        version = self.get_image_version(validated_data['images'])
        service_environment = None
        try:
            jira = JiraProjectVersion.objects.get(name=version)
            validated_data['jira_version'] = jira.id
        except JiraProjectVersion.DoesNotExist:
            logger.error("没有关联到 jira版本")
        if 'service_environment' in validated_data.keys():
            service_environment = validated_data.pop('service_environment')
        for key, value in validated_data.items():
            if not hasattr(instance, key):
                continue
            setattr(instance, key, value)
        if service_environment:
            instance.service_environment.set(service_environment)
        instance.save()
        return instance


class DBSerializer(serializers.ModelSerializer):
    rw_project = serializers.SlugRelatedField(source="project", slug_field='name', read_only=True)
    rw_environment = serializers.SlugRelatedField(source="environment", slug_field='environment', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = DB
        fields = "__all__"

    def validate(self, attrs):
        from utils.core.rsa_crypt import generator
        attrs['password'] = generator.decrypt_data(data=attrs['password'])
        return attrs


class NaCOSSerializer(serializers.ModelSerializer):
    rw_project = serializers.SlugRelatedField(source="project", slug_field='name', read_only=True)
    rw_environment = serializers.SlugRelatedField(source="environment", slug_field='environment', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = NaCOS
        fields = "__all__"

    def validate(self, attrs):
        from utils.core.rsa_crypt import generator
        attrs['password'] = generator.decrypt_data(data=attrs['password'])
        return attrs


class JenkinsSerializer(serializers.ModelSerializer):
    service_environment = ServiceEnvironmentSerializer(read_only=True)

    class Meta:
        model = Jenkins
        fields = "__all__"


__all__ = [
    'ProjectsSerializer',
    'EnvironmentSerializer',
    'KubernetesModelSerializer',
    'SSHKeySerializer',
    'ServiceConfigSerializer',
    'ServicesSerializer',
    'ServiceResourceSerializer',
    'KubernetesEnvironmentConfigurationSerializer',
    'DockerEnvironmentConfigurationSerializer',
    'ServiceEnvironmentSerializer',
    'KubernetesHelmRepoModelSerializer',
    'KubernetesHelmChartModelSerializer',
    'ProductsSerializer',
    'DBSerializer',
    'NaCOSSerializer',
    'NoticeSerializer',
    'EnvironmentVariableSerializer',
    'JenkinsSerializer',
    'ContentTypeSerializer'
]

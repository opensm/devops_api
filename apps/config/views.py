from apps.config.models import *
from apps.config.serializers import *
from utils.core.views import *


class ProjectManagerView(ListCreateAPIView):
    serializer_class = ProjectsSerializer
    model = Projects


class ProjectUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectsSerializer
    model = Projects


class NoticeManagerView(ListCreateAPIView):
    serializer_class = NoticeSerializer
    model = Notice


class NoticeUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = NoticeSerializer
    model = Notice


class EnvironmentVariableManagerView(ListCreateAPIView):
    serializer_class = EnvironmentVariableSerializer
    model = EnvironmentVariable


class EnvironmentVariableUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = EnvironmentVariableSerializer
    model = EnvironmentVariable


class EnvironmentManagerView(ListCreateAPIView):
    serializer_class = EnvironmentSerializer
    model = Environment


class EnvironmentUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = EnvironmentSerializer
    model = Environment


class KubernetesModelManagerView(ListCreateAPIView):
    serializer_class = KubernetesModelSerializer
    model = KubernetesModel


class KubernetesModelUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = KubernetesModelSerializer
    model = KubernetesModel


class SSHKeyManagerView(ListCreateAPIView):
    serializer_class = SSHKeySerializer
    model = SSHKey


class SSHKeyUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = SSHKeySerializer
    model = SSHKey


class ServiceConfigManagerView(ListCreateAPIView):
    serializer_class = ServiceConfigSerializer
    model = ServiceConfig


class ServiceConfigUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceConfigSerializer
    model = ServiceConfig


class ServicesManagerView(ListCreateAPIView):
    serializer_class = ServicesSerializer
    model = Services


class ServicesUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = ServicesSerializer
    model = Services


class ServiceResourceManagerView(ListCreateAPIView):
    serializer_class = ServiceResourceSerializer
    model = ServiceResource


class ServiceResourceUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceResourceSerializer
    model = ServiceResource


class KubernetesEnvironmentConfigurationManagerView(ListCreateAPIView):
    serializer_class = KubernetesEnvironmentConfigurationSerializer
    model = KubernetesEnvironmentConfiguration


class KubernetesEnvironmentConfigurationUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = KubernetesEnvironmentConfigurationSerializer
    model = KubernetesEnvironmentConfiguration


class DockerEnvironmentConfigurationManagerView(ListCreateAPIView):
    serializer_class = DockerEnvironmentConfigurationSerializer
    model = DockerEnvironmentConfiguration


class DockerEnvironmentConfigurationUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = DockerEnvironmentConfigurationSerializer
    model = DockerEnvironmentConfiguration


class ServiceEnvironmentManagerView(ListCreateAPIView):
    serializer_class = ServiceEnvironmentSerializer
    model = ServiceEnvironment


class ServiceEnvironmentUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceEnvironmentSerializer
    model = ServiceEnvironment


class KubernetesHelmRepoModelManagerView(ListCreateAPIView):
    serializer_class = KubernetesHelmRepoModelSerializer
    model = KubernetesHelmRepoModel


class KubernetesHelmRepoModelUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = KubernetesHelmRepoModelSerializer
    model = KubernetesHelmRepoModel


class KubernetesHelmChartModelManagerView(ListCreateAPIView):
    serializer_class = KubernetesHelmChartModelSerializer
    model = KubernetesHelmChartModel


class KubernetesHelmChartModelUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = KubernetesHelmChartModelSerializer
    model = KubernetesHelmChartModel


class ProductsManagerView(ListCreateAPIView):
    serializer_class = ProductsSerializer
    model = Products


class ProductsUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductsSerializer
    model = Products


class DBManagerView(ListCreateAPIView):
    serializer_class = DBSerializer
    model = DB


class DBUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = DBSerializer
    model = DB


class NaCOSManagerView(ListCreateAPIView):
    serializer_class = NaCOSSerializer
    model = NaCOS


class NaCOSUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = NaCOSSerializer
    model = NaCOS


class JenkinsManagerView(ListCreateAPIView):
    serializer_class = JenkinsSerializer
    model = Jenkins


class JenkinsUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = JenkinsSerializer
    model = Jenkins


__all__ = [
    'JenkinsManagerView',
    'JenkinsUpdateView',
    'ProjectManagerView',
    'ProjectUpdateView',
    'EnvironmentManagerView',
    'EnvironmentUpdateView',
    'KubernetesModelManagerView',
    'KubernetesModelUpdateView',
    'SSHKeyManagerView',
    'SSHKeyUpdateView',
    'ServiceConfigManagerView',
    'ServiceConfigUpdateView',
    'ServicesManagerView',
    'ServicesUpdateView',
    'ServiceResourceManagerView',
    'ServiceResourceUpdateView',
    'KubernetesEnvironmentConfigurationManagerView',
    'KubernetesEnvironmentConfigurationUpdateView',
    'DockerEnvironmentConfigurationManagerView',
    'DockerEnvironmentConfigurationUpdateView',
    'ServiceEnvironmentManagerView',
    'ServiceEnvironmentUpdateView',
    'KubernetesHelmRepoModelManagerView',
    'KubernetesHelmRepoModelUpdateView',
    'KubernetesHelmChartModelManagerView',
    'KubernetesHelmChartModelUpdateView',
    'ProductsManagerView',
    'ProductsUpdateView',
    'DBManagerView',
    'DBUpdateView',
    'NaCOSManagerView',
    'NaCOSUpdateView',
    'NoticeManagerView',
    'NoticeUpdateView',
    'EnvironmentVariableUpdateView',
    'EnvironmentVariableManagerView'
]

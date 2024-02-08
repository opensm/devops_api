"""devops_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from apps.config.views import *

urlpatterns = [
    path('projects', ProjectManagerView.as_view(), name="projects"),
    re_path('project/(?P<pk>\d+)$', ProjectUpdateView.as_view(), name="project"),
    path('environments', EnvironmentManagerView.as_view(), name="environments"),
    re_path('environment/(?P<pk>\d+)$', EnvironmentUpdateView.as_view(), name="environment"),
    path('environment_variables', EnvironmentVariableManagerView.as_view(), name="environment_variables"),
    re_path('environment_variable/(?P<pk>\d+)$', EnvironmentVariableUpdateView.as_view(), name="environment_variable"),
    path('kubernetes', KubernetesModelManagerView.as_view(), name="kubernetes"),
    re_path('kubernetes_info/(?P<pk>\d+)$', KubernetesModelUpdateView.as_view(), name="kubernetes_info"),
    path('sshkeys', SSHKeyManagerView.as_view(), name="sshkeys"),
    re_path('sshkey/(?P<pk>\d+)$', SSHKeyUpdateView.as_view(), name="sshkey"),
    path('service_configs', ServiceConfigManagerView.as_view(), name="service_configs"),
    re_path('service_config/(?P<pk>\d+)$', ServiceConfigUpdateView.as_view(), name="service_config"),
    path('services', ServicesManagerView.as_view(), name="services"),
    re_path('service/(?P<pk>\d+)$', ServicesUpdateView.as_view(), name="service"),
    path('service_resources', ServiceResourceManagerView.as_view(), name="service_resources"),
    re_path('service_resource/(?P<pk>\d+)$', ServiceResourceUpdateView.as_view(), name="service_resource"),
    path('kubernetes_environment_configurations',
         KubernetesEnvironmentConfigurationManagerView.as_view(),
         name="kubernetes_environment_configurations"),
    re_path('kubernetes_environment_configuration/(?P<pk>\d+)$', EnvironmentUpdateView.as_view(),
            name="kubernetes_environment_configuration"),
    path('docker_environment_configurations',
         DockerEnvironmentConfigurationManagerView.as_view(),
         name="docker_environment_configurations"),
    re_path('docker_environment_configuration/(?P<pk>\d+)$',
            DockerEnvironmentConfigurationUpdateView.as_view(),
            name="docker_environment_configuration"),
    path('service_environments', ServiceEnvironmentManagerView.as_view(), name="service_environments"),
    re_path('service_environment/(?P<pk>\d+)$', ServiceEnvironmentUpdateView.as_view(), name="service_environment"),
    path('kubernetes_helm_repos', KubernetesHelmRepoModelManagerView.as_view(), name="kubernetes_helm_repos"),
    re_path('kubernetes_helm_repo/(?P<pk>\d+)$', KubernetesHelmRepoModelUpdateView.as_view(), name="environment"),
    path('kubernetes_helm_charts', KubernetesHelmChartModelManagerView.as_view(), name="kubernetes_helm_charts"),
    re_path('kubernetes_helm_chart/(?P<pk>\d+)$', KubernetesHelmChartModelUpdateView.as_view(),
            name="kubernetes_helm_chart"),
    path('products', ProductsManagerView.as_view(), name="products"),
    re_path('product/(?P<pk>\d+)$', ProductsUpdateView.as_view(), name="product"),
    path('dbs', DBManagerView.as_view(), name="dbs"),
    re_path('db/(?P<pk>\d+)$', DBUpdateView.as_view(), name="db"),
    path('nacoses', NaCOSManagerView.as_view(), name="nacoses"),
    re_path('nacos/(?P<pk>\d+)$', NaCOSUpdateView.as_view(), name="nacos"),
    path('notices', NoticeManagerView.as_view(), name="notices"),
    re_path('notice/(?P<pk>\d+)$', NoticeUpdateView.as_view(), name="notice"),
    path('jenkins_all', JenkinsManagerView.as_view(), name="jenkins_all"),
    re_path('jenkins/(?P<pk>\d+)$', JenkinsUpdateView.as_view(), name="jenkins"),
    path('contents', ContentListView.as_view(), name="contents")
]

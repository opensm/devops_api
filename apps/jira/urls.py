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
from apps.jira.views import *

urlpatterns = [
    path('jiraes', JiraModelManagerView.as_view(), name="jiraes"),
    re_path('jira/(?P<pk>\d+)$', JiraModelUpdateView.as_view(), name="jira"),

    path('jira_projects', JiraProjectManagerView.as_view(), name="jira_projects"),
    re_path('jira_project/(?P<pk>\d+)$', JiraProjectUpdateView.as_view(), name="jira_project"),

    path('jira_project_versions', JiraProjectVersionManagerView.as_view(), name="jira_project_versions"),
    re_path('jira_project_version/(?P<pk>\d+)$', JiraProjectVersionUpdateView.as_view(), name="jira_project_version"),
]

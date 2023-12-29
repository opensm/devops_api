from apps.jira.models import *
from apps.jira.serializers import *
from utils.core.views import *


class JiraModelManagerView(ListCreateAPIView):
    serializer_class = JiraModelSerializer
    model = JiraModel


class JiraModelUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = JiraModelSerializer
    model = JiraModel


class JiraProjectManagerView(ListCreateAPIView):
    serializer_class = JiraProjectSerializer
    model = JiraProject


class JiraProjectUpdateView(UpdateAPIView):
    serializer_class = JiraModelSerializer
    model = JiraProject


class JiraProjectVersionManagerView(ListCreateAPIView):
    serializer_class = JiraProjectVersionSerializer
    model = JiraProjectVersion


class JiraProjectVersionUpdateView(RetrieveUpdateAPIView):
    serializer_class = JiraProjectVersionSerializer
    model = JiraProjectVersion


__all__ = [
    'JiraModelManagerView',
    'JiraModelUpdateView',
    'JiraProjectManagerView',
    'JiraProjectUpdateView',
    'JiraProjectVersionManagerView',
    'JiraProjectVersionUpdateView'
]

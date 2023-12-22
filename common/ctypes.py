from django.contrib.contenttypes.models import ContentType


def get_content_type(obj):
    return ContentType.objects.get_for_model(obj)

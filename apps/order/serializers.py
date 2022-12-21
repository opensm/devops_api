from rest_framework import serializers
from apps.order.models import *

class KubernetesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesModel
        fields = "__all__"

class KubernetesNameSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesNameSpace
        fields = "__all__"

class KubernetesWorkLoadServiceIngressTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesWorkLoadServiceIngressTemplate
        fields = "__all__"


class DBSerializer(serializers.ModelSerializer):
    class Meta:
        model = DB
        fields = "__all__"

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"

__all__ = ['KubernetesModelSerializer','KubernetesNameSpaceSerializer','KubernetesWorkLoadServiceIngressTemplateSerializer','DBSerializer','OrdersSerializer']
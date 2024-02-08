from apps.order.models import *
from apps.order.serializers import *
from utils import *
from utils.core.views import *
from django.contrib.contenttypes.models import ContentType


class ContentTypeListView(ListAPIView):
    serializer_class = ContentTypeSerializer
    model = ContentType

    def get_queryset(self):
        queryset = ContentType.objects.filter(
            model__in=['db', 'nacos', 'kuberneteshelmchartmodel']
        )
        return queryset


class OrdersManagerView(ListCreateAPIView):
    serializer_class = OrdersSerializer
    model = Orders


class OrdersUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrdersSerializer
    model = Orders


class OrderManagerView(ListCreateAPIView):
    serializer_class = OrderSerializer
    model = Order


class OrderUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    model = Order


class JenkinsOrdersManagerView(ListCreateAPIView):
    serializer_class = JenkinsOrdersSerializer
    model = JenkinsOrders


class JenkinsOrdersGetView(RetrieveAPIView):
    serializer_class = JenkinsOrdersSerializer
    model = JenkinsOrders


__all__ = [
    'ContentTypeListView',
    'OrderManagerView',
    'OrderUpdateView',
    'OrdersManagerView',
    'OrdersUpdateView',
    'JenkinsOrdersManagerView',
    'JenkinsOrdersGetView'
]

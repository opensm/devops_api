from rest_framework.views import APIView
from utils.response import *
from apps.order.models import *
from apps.order.serializers import *

# Create your views here.

class KubernetesNamespaceRsyncController(APIView):

    def get(self, request, *args, **kwargs):
        kubernetes_id = request.GET.get("id")
        try:
            data = KubernetesModel.objects.get(id=kubernetes_id)
        except Exception as e:
            return DataResponse(code=20001,message="获取集群信息异常！")

class KubernetesManager(APIView):

    def get(self, requests, **kwargs):
        if not kwargs:
            object_data = KubernetesModel.objects.all()
        else:
            object_data = KubernetesModel.objects.filter(**kwargs)
        
        

        data = KubernetesModelSerializer(instance=object_data, many=True)
        print(data.data)
        # data_results = { "data": data.data,"total": len(data.data)}

        return DataResponse(data=data.data, message="获取集群信息成功！", code=20000,total=len(data.data))

    def put(self, request, **kwargs):
        object_data = KubernetesModel.objects.filter(id=request.data.get('id'))
        if not object_data:
            return DataResponse(message="获取更新数据错误", code=20002)
        for x in object_data:
            serializer_data = KubernetesModelSerializer(
                instance=x, data=request.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                x.save()

        return DataResponse(message="更新数据成功！", code=20000)

    def delete(self, requests, **kwargs):
        """
        :param requests:
        :param kwargs:
        :return:
        """
        if not kwargs:
            return DataResponse(message="输入参数错误！", code=20001)
        KubernetesModel.objects.filter(**kwargs).delete()
        return DataResponse(message="更新数据成功！", code=20000)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        if not requests.data:
            return DataResponse(message="请求参数错误！", code=20001)
        else:
            serializer_data = KubernetesModelSerializer(data=requests.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                serializer_data.save()
                return DataResponse(message="更新数据成功！", code=20000)


class KubernetesNameSpaceManager(APIView):

    def get(self, requests, **kwargs):
        if not kwargs:
            object_data = KubernetesNameSpace.objects.all()
        else:
            object_data = KubernetesNameSpace.objects.filter(**kwargs)

        data = KubernetesNameSpaceSerializer(instance=object_data, many=True)

        return DataResponse(data=data.data, message="获取集群命名空间信息成功！", code=20000)


class KubernetesWorkLoadServiceIngressTemplateManager(APIView):

    def get(self, requests, **kwargs):
        if not kwargs:
            object_data = KubernetesWorkLoadServiceIngressTemplate.objects.all()
        else:
            object_data = KubernetesWorkLoadServiceIngressTemplate.objects.filter(
                **kwargs)

        data = KubernetesWorkLoadServiceIngressTemplateSerializer(
            instance=object_data, many=True)

        return DataResponse(data=data.data, message="获取kubernetes模板信息成功！", code=20000)

    def put(self, requests, **kwargs):
        if not kwargs:
            return DataResponse(message="输入参数错误！", code=20001)
        object_data = KubernetesWorkLoadServiceIngressTemplate.objects.filter(
            **kwargs)
        if not object_data:
            return DataResponse(message="获取更新数据错误", code=20002)
        for x in object_data:
            serializer_data = KubernetesWorkLoadServiceIngressTemplateSerializer(
                instance=x, data=requests.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                x.save()

        return DataResponse(message="更新数据成功！", code=20000)

    def delete(self, requests, **kwargs):
        """
        :param requests:
        :param kwargs:
        :return:
        """
        KubernetesWorkLoadServiceIngressTemplate.objects.filter(
            **kwargs).delete()
        return DataResponse(message="更新数据成功！", code=20000)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        if not requests.data:
            return DataResponse(message="请求参数错误！", code=20001)
        else:
            serializer_data = KubernetesModelSerializer(data=requests.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                serializer_data.save()
                return DataResponse(message="更新数据成功！", code=20000)


class DBManager(APIView):

    def get(self, requests, **kwargs):
        if not kwargs:
            object_data = DB.objects.all()
        else:
            object_data = DB.objects.filter(**kwargs)

        data = DBSerializer(instance=object_data, many=True)

        return DataResponse(data=data.data, message="获取集群信息成功！", code=20000)

    def put(self, requests, **kwargs):
        if not kwargs:
            return DataResponse(message="输入参数错误！", code=20001)
        object_data = DB.objects.filter(**kwargs)
        if not object_data:
            return DataResponse(message="获取更新数据错误", code=20002)
        for x in object_data:
            serializer_data = DBSerializer(instance=x, data=requests.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                x.save()

        return DataResponse(message="更新数据成功！", code=20000)

    def delete(self, requests, **kwargs):
        """
        :param requests:
        :param kwargs:
        :return:
        """
        DB.objects.filter(**kwargs).delete()
        return DataResponse(message="更新数据成功！", code=20000)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        if not requests.data:
            return DataResponse(message="请求参数错误！", code=20001)
        else:
            serializer_data = DBSerializer(data=requests.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                serializer_data.save()
                return DataResponse(message="更新数据成功！", code=20000)


class OrdersManager(APIView):

    def get(self, requests, **kwargs):
        if not kwargs:
            object_data = Orders.objects.all()
        else:
            object_data = Orders.objects.filter(**kwargs)

        data = OrdersSerializer(instance=object_data, many=True)

        return DataResponse(data=data.data, message="获取集群信息成功！", code=20000)

    def put(self, requests, **kwargs):
        if not kwargs:
            return DataResponse(message="输入参数错误！", code=20001)
        object_data = Orders.objects.filter(**kwargs)
        if not object_data:
            return DataResponse(message="获取更新数据错误", code=20002)
        for x in object_data:
            serializer_data = OrdersSerializer(instance=x, data=requests.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                x.save()

        return DataResponse(message="更新数据成功！", code=20000)

    def delete(self, requests, **kwargs):
        """
        :param requests:
        :param kwargs:
        :return:
        """
        OrdersSerializer.objects.filter(**kwargs).delete()
        return DataResponse(message="更新数据成功！", code=20000)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        if not requests.data:
            return DataResponse(message="请求参数错误！", code=20001)
        else:
            serializer_data = OrdersSerializer(data=requests.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                serializer_data.save()
                return DataResponse(message="更新数据成功！", code=20000)


__all__ = [
    'KubernetesManager', 
    'KubernetesNameSpaceManager',
    'KubernetesWorkLoadServiceIngressTemplateManager',
    'DBManager',
    'OrdersManager'
]

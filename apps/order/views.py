from rest_framework.views import APIView
from utils.response import *
from apps.order.models import *
from apps.order.serializers import *
# from utils.kubernetes import KubernetesClass
# from utils.exceptions import *
# from utils.requests import *
from utils import *

# Create your views here.

class KubernetesNamespaceRsyncController(APIView):

    def get(self, request, *args, **kwargs):
        try:
            _kwargs = format_request_params(request=request,model=KubernetesModel)
            data = KubernetesModel.objects.get(**_kwargs)
            k8s = KubernetesClass()
            k8s.connect(obj=data,api_type="CoreV1Api")
            namespaces=k8s.list_namespace()
            for namespace in namespaces:
                print(namespace)
        except KubernetesModel.DoesNotExist:
            return DataResponse(code=40001,message="Couldn't find Kubernetes message.")
        except PermissionDeniedException as exc:
            return DataResponse(code=exc.code,message=exc.message)
        except Exception as e:
            return DataResponse(code=20001,message="获取集群信息异常,error:{}".format(e))

class KubernetesManager(APIView):

    def get(self, request, **kwargs):
        try:
            _kwargs = format_request_params(request=request,model=KubernetesModel)
            if not kwargs:
                object_data = KubernetesModel.objects.all()
            else:
                object_data = KubernetesModel.objects.filter(**kwargs)
            
            data = KubernetesModelSerializer(instance=object_data, many=True)
            return DataResponse(data=data.data, message="获取集群信息成功！", code=20000,total=len(data.data))
        except ParamErrorException as error:
            return DataResponse(code=error.code,message=error.message)

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
                serializer_data.save()

        return DataResponse(message="更新数据成功！", code=20000)

    def delete(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        try:
            _kwargs = format_request_params(request=request,model=KubernetesModel)
            if not _kwargs:
                return DataResponse(message="输入参数错误！", code=20001)
            KubernetesModel.objects.filter(**_kwargs).delete()
            return DataResponse(message="更新数据成功！", code=20000)
        except ParamErrorException as error:
            return DataResponse(message=error.message, code=error.code)

    def post(self, request):
        """
        :param request:
        :return:
        """
        if not request.data:
            return DataResponse(message="请求参数错误！", code=20001)
        else:
            serializer_data = KubernetesModelSerializer(data=request.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                serializer_data.save()
                return DataResponse(message="更新数据成功！", code=20000)


class KubernetesNameSpaceManager(APIView):

    def get(self, request, **kwargs):
        try:
            _kwargs = format_request_params(request=request,model=KubernetesNameSpace)
            if not _kwargs:
                object_data = KubernetesNameSpace.objects.all()
            else:
                object_data = KubernetesNameSpace.objects.filter(**_kwargs)

            data = KubernetesNameSpaceSerializer(instance=object_data, many=True)

            return DataResponse(data=data.data, message="获取集群命名空间信息成功！", code=20000)
        except ParamErrorException as error:
            return DataResponse(message=error.message, code=error.code)


class KubernetesWorkLoadServiceIngressTemplateManager(APIView):

    def get(self, request, **kwargs):
        _kwargs = format_request_params(request=request,model=KubernetesWorkLoadServiceIngressTemplate)
        if not _kwargs:
            object_data = KubernetesWorkLoadServiceIngressTemplate.objects.all()
        else:
            object_data = KubernetesWorkLoadServiceIngressTemplate.objects.filter(
                **_kwargs
            )

        data = KubernetesWorkLoadServiceIngressTemplateSerializer(
            instance=object_data, many=True
        )

        return DataResponse(data=data.data, message="获取kubernetes模板信息成功!", code=20000)

    def put(self, request, **kwargs):
        try:
            _kwargs = format_request_params(request=request,model=KubernetesWorkLoadServiceIngressTemplate)
            if not _kwargs:
                return DataResponse(message="输入参数错误！", code=20001)
            object_data = KubernetesWorkLoadServiceIngressTemplate.objects.filter(
                **_kwargs
            )
            if not object_data:
                return DataResponse(message="获取更新数据错误", code=20002)
            for x in object_data:
                serializer_data = KubernetesWorkLoadServiceIngressTemplateSerializer(
                    instance=x, data=request.data)
                if not serializer_data.is_valid():
                    return DataResponse(message=serializer_data.errors, code=20002)
                else:
                    x.save()

            return DataResponse(message="更新数据成功！", code=20000)
        except ParamErrorException as error:
            return DataResponse(message=error.message, code=error.code)
    

    def delete(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        try:
            _kwargs = format_request_params(request=request,model=KubernetesWorkLoadServiceIngressTemplate)
            KubernetesWorkLoadServiceIngressTemplate.objects.filter(
                **_kwargs
            ).delete()
            return DataResponse(message="更新数据成功！", code=20000)
        except ParamErrorException as error:
            return DataResponse(message=error.message, code=error.code)

    def post(self, request):
        """
        :param request:
        :return:
        """
        if not request.data:
            return DataResponse(message="请求参数错误！", code=20001)
        else:
            serializer_data = KubernetesModelSerializer(data=request.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                serializer_data.save()
                return DataResponse(message="更新数据成功！", code=20000)


class DBManager(APIView):

    def get(self, request, **kwargs):
        try:
            _kwargs = format_request_params(request=request,model=DB)
            if not _kwargs:
                object_data = DB.objects.all()
            else:
                object_data = DB.objects.filter(**_kwargs)
            data = DBSerializer(instance=object_data, many=True)
            return DataResponse(data=data.data, message="获取集群信息成功！", code=20000)
        except ParamErrorException as error:
            return DataResponse(message=error.message, code=error.code)

    def put(self, request, **kwargs):
        try:
            _kwargs = format_request_params(request=request,model=DB)
            if not _kwargs:
                return DataResponse(message="输入参数错误！", code=20001)
            object_data = DB.objects.filter(**_kwargs)
            if not object_data:
                return DataResponse(message="获取更新数据错误", code=20002)
            for x in object_data:
                serializer_data = DBSerializer(instance=x, data=request.data)
                if not serializer_data.is_valid():
                    return DataResponse(message=serializer_data.errors, code=20002)
                else:
                    x.save()

            return DataResponse(message="更新数据成功！", code=20000)
        except ParamErrorException as error:
            return DataResponse(message=error.message, code=error.code)

    def delete(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        try:
            _kwargs = format_request_params(request=request,model=DB)
            DB.objects.filter(**_kwargs).delete()
            return DataResponse(message="更新数据成功！", code=20000)
        except ParamErrorException as error:
            return DataResponse(message=error.message, code=error.code)

    def post(self, request):
        """
        :param request:
        :return:
        """
        if not request.data:
            return DataResponse(message="请求参数错误！", code=20001)
        else:
            serializer_data = DBSerializer(data=request.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                serializer_data.save()
                return DataResponse(message="更新数据成功！", code=20000)


class OrdersManager(APIView):

    def get(self, request, **kwargs):
        try:
            _kwargs = format_request_params(request=request,model=Orders)
            if not _kwargs:
                object_data = Orders.objects.all()
            else:
                object_data = Orders.objects.filter(**_kwargs)
            data = OrdersSerializer(instance=object_data, many=True)
            return DataResponse(data=data.data, message="获取集群信息成功！", code=20000)
        except ParamErrorException as error:
            return DataResponse(message=error.message, code=error.code)

    def put(self, request, **kwargs):
        try:
            _kwargs = format_request_params(request=request,model=Orders)
            if not kwargs:
                return DataResponse(message="输入参数错误！", code=20001)
            object_data = Orders.objects.filter(**_kwargs)
            if not object_data:
                return DataResponse(message="获取更新数据错误", code=20002)
            for x in object_data:
                serializer_data = OrdersSerializer(instance=x, data=request.data)
                if not serializer_data.is_valid():
                    return DataResponse(message=serializer_data.errors, code=20002)
                else:
                    x.save()
            return DataResponse(message="更新数据成功！", code=20000)
        except ParamErrorException as error:
            return DataResponse(message=error.message, code=error.code)

    def delete(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        try:
            _kwargs = format_request_params(request=request,model=Orders)
            OrdersSerializer.objects.filter(**_kwargs).delete()
            return DataResponse(message="更新数据成功！", code=20000)
        except ParamErrorException as error:
            return DataResponse(message=error.message, code=error.code)

    def post(self, request):
        """
        :param request:
        :return:
        """
        if not request.data:
            return DataResponse(message="请求参数错误！", code=20001)
        else:
            serializer_data = OrdersSerializer(data=request.data)
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
    'OrdersManager',
    'KubernetesNamespaceRsyncController'
]

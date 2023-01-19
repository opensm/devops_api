from rest_framework.views import APIView
from utils.response import *
from apps.account.serializers import *
from django.utils import timezone
from apps.account.models import *


class UserManager(APIView):

    def get(self, request, **kwargs):
        """
        获取用户信息
        :param request:
        :param kwargs:
        :return:
        """
        if not kwargs:
            object_data = User.objects.all()
        else:
            object_data = User.objects.filter(**kwargs)
        print(object_data)
        data = UserSerializer(instance=object_data,many=True)

        return DataResponse(data=data.data, message="获取用户信息成功！", code=20000)

    def put(self, request, **kwargs):

        if not request.data:
            return DataResponse(
                message="请正确请求接口",
                code=20001,
            )
        if not kwargs:
            object_data = User.objects.all()
        else:
            object_data = User.objects.filter(**kwargs)
        for x in object_data:
            obj = UserSerializer(instance=x,data=request.data)
            if not obj.is_valid():
                return DataResponse(
                    message=obj.errors,
                    code=obj.non_field_errors(),
                )
            else:
                obj.save()
        return DataResponse(message="操作成功！", code=20000)

    def delete(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        if not kwargs:
           return DataResponse(message="操作异常，请检查删除的内容！", code=20001)
        User.objects.filter(**kwargs).delete()
        return DataResponse(message="删除操作成功！", code=20000)

    def post(self, request):
        """
        :param request:
        :return:
        """
        obj = UserSerializer(data=request.data)
        if not obj.is_valid():
            return DataResponse(
                    message=obj.errors,
                    code=obj.non_field_errors(),
                )
        else:
            obj.save()
        return DataResponse(message="添加操作成功！", data=request.data,code=20000)


class Menu(APIView):

    def get(self, request):
        data = [{
            "path": "/",
            "component": "Layout",
            "hidden": True,
            "icon": "dashboard",
            "name": "login"
        }, {
            "path": "/404",
            "component": "@/views/404",
            "hidden": True
        }]
        return DataResponse(data=data, message="获取用户信息成功！", code=20000)


class CurrentUser(APIView):
    def get(self, request):
        print(request.data)
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            instance = UserToken.objects.get(token=token)
            data = {
                'username': instance.username.username,
                'name': instance.username.name,
                'email': instance.username.email,
                'mobile': instance.username.mobile,
                'ldap': instance.username.ldap,
                'avatar': 'https://tupian.qqw21.com/article/UploadPic/2020-4/202041422405279300.jpg',
                'roles': "admin"
            }
            return DataResponse(data=data, message="获取用户信息成功！", code=20000)
        except UserToken.DoesNotExist:
            return DataResponse(message="用户登录过期，请重新登录！", code=40001)
        except User.DoesNotExist:
            return DataResponse(message="获取用户信息失败！", code=40001)


class Login(APIView):
    def post(self, request):
        """
        :param request:
        :return:
        """
        print(request.data)
        data = SignInSerializer(data=request.data)
        if not data.is_valid():
            return APIResponse(
                data=[],
                code=40001,
                message="登录失败,用户或账号密码错误！"
            )

        # 保存(存在就更新不存在就创建，并设置过期时间为60分钟)
        expiration_time = timezone.now() + timezone.timedelta(minutes=+60)
        try:
            user = User.objects.get(username=data.data['username'])
            token_data = {'username': user.id, 'expiration_time': expiration_time}
            obj = UserTokenSerializer(data=token_data)
            if not obj.is_valid():
                raise Exception("密钥生成失败！")
            obj.save()
            return DataResponse(
                code=20000,
                message="登录成功!",
                data={"token": obj.data['token']}
            )
        except Exception as e:
            return DataResponse(
                code=40001,
                message="登录失败,用户token更新失败,{0}".format(e)
            )

    def get(self, request):
        """
        :param request:
        :return:
        """
        print(request.data)
        return APIResponse(data="ddddddd", status=200)


class Logout(APIView):
    def post(self, request):
        """
        :param request:
        :return:
        """
        print(request.data)
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            UserToken.objects.get(token=token).delete()
            return DataResponse(message="推出登录成功！", code=20000)
        except User.DoesNotExist:
            return DataResponse(message="推出登录失败！", code=40001)

    def get(self, request):
        """
        :param request:
        :return:
        """
        print(request.data)
        return APIResponse(data="ddddddd", status=200)


class RoleManager(APIView):
    def get(self, request, **kwargs):
        print(request.data)
        return APIResponse(data="dddd", status=200)

    def put(self, request, **kwargs):
        print(request.data)
        return APIResponse(data="dddd", status=200)

    def delete(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        print(request.data)
        return APIResponse(data="dddd", status=200)

    def post(self, request):
        """
        :param request:
        :return:
        """
        print(request.data)
        return APIResponse(data="dddd", status=200)


class PermissionManager(APIView):
    def get(self, request, **kwargs):
        print(request.data)
        return APIResponse(data="dddd", status=200)

    def put(self, request, **kwargs):
        print(request.data)
        return APIResponse(data="dddd", status=200)

    def delete(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        print(request.data)
        return APIResponse(data="dddd", status=200)

    def post(self, request):
        """
        :param request:
        :return:
        """
        print(request.data)
        return APIResponse(data="dddd", status=200)



class LDAPManager(APIView):
    
    def get(self, requests, **kwargs):
        if not kwargs:
            object_data = GlobalLdapConfiguration.objects.all()
        else:
            object_data = GlobalLdapConfiguration.objects.filter(**kwargs)
        
        

        data = GlobalLdapConfigurationSerializer(instance=object_data, many=True)
        print(data.data)
        # data_results = { "data": data.data,"total": len(data.data)}

        return DataResponse(data=data.data, message="获取集群信息成功！", code=20000,total=len(data.data))

    def put(self, request, **kwargs):
        object_data = GlobalLdapConfiguration.objects.filter(id=request.data.get('id'))
        if not object_data:
            return DataResponse(message="获取更新数据错误", code=20002)
        for x in object_data:
            serializer_data = GlobalLdapConfigurationSerializer(
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
        GlobalLdapConfiguration.objects.filter(**kwargs).delete()
        return DataResponse(message="更新数据成功！", code=20000)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        if not requests.data:
            return DataResponse(message="请求参数错误！", code=20001)
        else:
            serializer_data = GlobalLdapConfigurationSerializer(data=requests.data)
            if not serializer_data.is_valid():
                return DataResponse(message=serializer_data.errors, code=20002)
            else:
                serializer_data.save()
                return DataResponse(message="更新数据成功！", code=20000)
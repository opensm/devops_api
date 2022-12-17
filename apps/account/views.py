from rest_framework.views import APIView
from utils.response import *
from apps.account.serializers import *
from django.utils import timezone
from apps.account.models import *


class UserManager(APIView):

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
                'roles': [{
                    "path": "/auth",
                    "component": "Layout",
                    "hidden": False,
                    "icon": "dashboard",
                    "name": "auth",
                    "children": {

                    }
                }]
            }
            return DataResponse(data=data, message="获取用户信息成功！", code=20000)
        except User.DoesNotExist:
            return DataResponse(message="获取用户信息失败！", code=40001)


class Login(APIView):
    def post(self, request):
        """
        :param request:
        :return:
        """
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
                message="登录失败，用户token更新失败，{0}".format(e)
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

from rest_framework.views import APIView
from utils.response import APIResponse
from apps.account.serializers import *
from django.utils import timezone
from apps.account.models import *


class UserManager(APIView):

    def get(self, requests, **kwargs):
        print(requests.data)
        return APIResponse(data="dddd", status=200)

    def put(self, requests, **kwargs):
        print(requests.data)
        return APIResponse(data="dddd", status=200)

    def delete(self, requests, **kwargs):
        """
        :param requests:
        :param kwargs:
        :return:
        """
        print(requests.data)
        return APIResponse(data="dddd", status=200)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        print(requests.data)
        return APIResponse(data="dddd", status=200)


class Login(APIView):
    def post(self, requests):
        """
        :param requests:
        :return:
        """
        data = SignInSerializer(data=requests.data)
        if not data.is_valid():
            return APIResponse(
                data=[],
                status=200,
                errcode="00001",
                errmsg="登录失败,用户或账号密码错误！"
            )

        # 保存(存在就更新不存在就创建，并设置过期时间为60分钟)
        expiration_time = timezone.now() + timezone.timedelta(minutes=+60)
        # token = make_token(username=data.data['username'])
        try:
            user = User.objects.get(username=data.data['username'])
            data = {'username': user.id, 'expiration_time':expiration_time}
            obj = UserTokenSerializer(data=data)
            if not  obj.is_valid():
                raise Exception("密钥生成失败！")
            obj.save()
            return APIResponse(
                code="00000",
                msg="登录成功!",
                token=obj.token
            )
        except Exception as e:
            return APIResponse(
                code="00001",
                msg="登录失败，用户token更新失败，{0}".format(e)
            )

    def get(self, requests):
        """
        :param requests:
        :return:
        """
        print(requests.data)
        return APIResponse(data="ddddddd", status=200)


class Logout(APIView):
    def post(self, requests):
        """
        :param requests:
        :return:
        """
        print(requests.data)
        return APIResponse(data="ddddddd", status=200)

    def get(self, requests):
        """
        :param requests:
        :return:
        """
        print(requests.data)
        return APIResponse(data="ddddddd", status=200)


class RoleManager(APIView):
    def get(self, requests, **kwargs):
        print(requests.data)
        return APIResponse(data="dddd", status=200)

    def put(self, requests, **kwargs):
        print(requests.data)
        return APIResponse(data="dddd", status=200)

    def delete(self, requests, **kwargs):
        """
        :param requests:
        :param kwargs:
        :return:
        """
        print(requests.data)
        return APIResponse(data="dddd", status=200)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        print(requests.data)
        return APIResponse(data="dddd", status=200)


class PermissionManager(APIView):
    def get(self, requests, **kwargs):
        print(requests.data)
        return APIResponse(data="dddd", status=200)

    def put(self, requests, **kwargs):
        print(requests.data)
        return APIResponse(data="dddd", status=200)

    def delete(self, requests, **kwargs):
        """
        :param requests:
        :param kwargs:
        :return:
        """
        print(requests.data)
        return APIResponse(data="dddd", status=200)

    def post(self, requests):
        """
        :param requests:
        :return:
        """
        print(requests.data)
        return APIResponse(data="dddd", status=200)

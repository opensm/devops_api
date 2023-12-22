from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.account.serializers import *
from apps.account.models import *
from utils.core.views import *
from utils.exceptions import PermissionDeniedException

from utils.devops_api_log import logger


class UserObtainTokenPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except PermissionDeniedException:
            raise PermissionDeniedException(message="验证失败！")
        logger.info(serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GenericKeyView(APIView):

    def get(self, request, *args, **kwargs):
        from utils.core.rsa_crypt import secret_data
        return Response(
            data={"publickey": secret_data[1], "code": 20000, "detail": "公钥请求成功"},
            status=status.HTTP_200_OK
        )


class UserManagerView(ListCreateAPIView):
    serializer_class = UserSerializer
    model = User


class UserUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    model = User


class AdminSetPasswordUpdateView(UpdateAPIView):
    serializer_class = AdminSetPasswordSerializer
    model = User


class UserPasswordUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        from utils.core.rsa_crypt import generator
        print("PUT")
        try:
            user = request.user
            sec_passwd = request.data.get('password', None)
            password = generator.decrypt_data(data=sec_passwd)
            user.set_password(password)
            user.save()
        except Exception as e:
            logger.error("Error generating {}".format(e))
        return Response(
            data={"status": True, "code": 20000, "detail": "修改密码成功"},
            status=status.HTTP_200_OK
        )


class CheckUserPasswdView(APIView):
    queryset = None
    serializer_class = UserResetPasswordSerializer
    model = User

    def post(self, request, *args, **kwargs):
        from utils.core.rsa_crypt import generator

        print("Checking")
        self.queryset = request.user
        sec_passwd = request.data.get('old_password', None)
        password = generator.decrypt_data(data=sec_passwd)
        print(request.data.get('old_password'))
        print(password)
        if self.queryset.check_password(password):
            return Response(
                data={"status": True, "code": 20000, "detail": "密码检查成功"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={"status": False, "code": 20000, "detail": "密码检查不匹配"},
                status=status.HTTP_200_OK
            )


class RoleManagerView(ListCreateAPIView):
    serializer_class = RoleSerializer
    model = Role


class RoleUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoleSerializer
    model = Role


class PermissionManagerView(ListCreateAPIView):
    serializer_class = PermissionsSerializer
    model = Permissions


class PermissionUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = PermissionsSerializer
    model = Permissions


class GlobalLDAPManagerView(ListCreateAPIView):
    serializer_class = GlobalLdapConfigurationSerializer
    model = GlobalLdapConfiguration


class GlobalLDAPUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = GlobalLdapConfigurationSerializer
    model = GlobalLdapConfiguration


class GlobalLDAPPasswordUpdateView(UpdateAPIView):
    serializer_class = GlobalLdapConfigurationPasswordSerializer
    model = GlobalLdapConfiguration


__all__ = [
    'GlobalLDAPPasswordUpdateView',
    "GlobalLDAPUpdateView",
    "GlobalLDAPManagerView",
    "AdminSetPasswordUpdateView",
    "PermissionUpdateView",
    "PermissionManagerView",
    "UserPasswordUpdateView",
    "UserUpdateView",
    "UserManagerView",
    "UserObtainTokenPairView",
    "RoleManagerView",
    "RoleUpdateView",
    "GenericKeyView",
    "CheckUserPasswdView"
]

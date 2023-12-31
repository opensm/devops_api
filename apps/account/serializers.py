from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from django.utils.translation import gettext_lazy as _
from apps.account.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.exceptions import *
from utils.core.rsa_crypt import generator
from utils.devops_api_log import logger


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    def get_token(self, user: AuthUser) -> Token:
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['mobile'] = user.mobile
        token['name'] = user.name
        token['is_superuser'] = user.is_superuser
        token['roles'] = self.get_user_roles(user=user)
        return token

    @classmethod
    def get_user_roles(cls, user: AuthUser):
        if user.is_superuser or user.roles.manager:
            return ['admin']
        elif user.roles.manager:
            return ['manager']
        else:
            for per in user.roles.permission.all():
                if per.manager:
                    return ['project-manager']
                if per.app_permissions:
                    return ['project-approve']
            return ['project-user']

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        """
        留空用于ldap接入
        """
        from utils.core.rsa_crypt import secret_data
        attrs['password'] = generator.decrypt_data(data=attrs['password'])
        logger.info("解密后数据：{}".format(attrs))
        data = dict()
        print("留空用于ldap接入")
        print(attrs)
        if attrs:
            data['data'] = super().validate(attrs)
        data['public_key'] = secret_data[1]
        data['message'] = "登录成功！"
        data['code'] = 20000
        return data


class PermissionsSerializer(serializers.ModelSerializer):
    rw_project = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Permissions
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    permission_child = PermissionsSerializer(read_only=True, source='permission', many=True)

    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ['password']

    def create(self, validated_data):
        """
        :param validated_data:
        :return:
        """
        from django.contrib.auth.hashers import make_password
        validated_data['password'] = make_password("12345678")
        instance = super().create(validated_data)
        return instance


class UserResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('password',)

    def validate(self, attrs):
        from utils.core.rsa_crypt import generator
        attrs['password'] = generator.decrypt_data(data=attrs['password'])
        return attrs

    def update(self, instance, attrs):
        attrs['password'] = make_password(attrs['password'])
        instance.password = attrs['password']
        instance.save()
        return instance


class AdminSetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['password', ]
        # exclude = ['password']

    def validate(self, attrs):
        from utils.core.rsa_crypt import generator
        attrs['password'] = generator.decrypt_data(data=attrs['password'])
        return attrs

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['password'].decode('utf8'))
        instance.save()
        return instance


class GlobalLdapConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalLdapConfiguration
        # fields = "__all__"
        exclude = ['ldap_bindpass']


class GlobalLdapConfigurationPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalLdapConfiguration
        fields = ['ldap_bindpass', 'id']
        read_only_fields = ['id']


class GroupField(serializers.Field):

    def serializers_value(self, value: GlobalLdapGroup):
        if value.parent_group:
            self.serializers_value(value.parent_group)
        else:
            return value.group_code

    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        return self.serializers_value(value)


class GlobalLdapGroupSerializer(serializers.ModelSerializer):
    group_string = GroupField(read_only=True)

    class Meta:
        model = GlobalLdapGroup
        fields = "__all__"

    def update(self, instance, validated_data):
        from core import Adopter
        ad = Adopter(
            domain=instance.auth.ldap_base_dn,
            ip=instance.auth.ldap_server,
            ca_certs_file="",
            ca_certs_path="",
            pwd=instance.auth.ldap_binddn,
            user=instance.auth.ldap_binddn
        )
        ad.modify_user(**validated_data)

        pass

    def create(self, validated_data):
        pass


__all__ = [
    "RoleSerializer",
    "UserSerializer",
    "GlobalLdapConfigurationSerializer",
    "UserTokenObtainPairSerializer",
    "PermissionsSerializer",
    "GlobalLdapConfigurationPasswordSerializer",
    "UserResetPasswordSerializer",
    "AdminSetPasswordSerializer",
    "GlobalLdapGroupSerializer"
]

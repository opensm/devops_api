from abc import ABC
import datetime
from rest_framework import serializers
from utils.crypt import AesCrypt
from devops_api.settings import SALT_KEY, SECRET_KEY
from django.contrib import auth
from apps.account.models import *
from django.utils import timezone as datetime
import time
import hashlib
from utils.exceptions import *
from rest_framework import status


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        error_messages={
            "required": "缺少用户名字段."
        }
    )
    password = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        error_messages={
            "required": "缺少密码字段.",
            "min_length": "密码太短，至少8个字符."
        }
    )
    ldap = serializers.BooleanField(
        allow_null=False,
        default=False,
        error_messages={
            "required": "缺少LDAP字段."
        }
    )
    crypt = AesCrypt(model='ECB', iv='', encode_='utf-8', key=SALT_KEY)

    def validate(self, attrs):
        """
        :param attrs:
        :return:
        """
        if attrs['ldap'] and not GlobalLdapConfiguration.objects.all():
            raise serializers.ValidationError(detail="Login failed,Ldap user not exist!", code="auth")
        try:
            attrs['password'] = self.crypt.aesdecrypt(attrs['password'])
            user_obj = auth.authenticate(**attrs)
            if not user_obj:
                raise serializers.ValidationError(detail="Login failed,user or password is not correct!{}".format(attrs), code="auth")
            User.objects.filter(**attrs).update(last_login=datetime.now())
        except ContentErrorException as exc:
            raise serializers.ValidationError(message=exc.message,code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except serializers.ValidationError as err:
            raise serializers.ValidationError(detail=err.detail, code=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            raise serializers.ValidationError(detail="User not exist!", code=status.HTTP_401_UNAUTHORIZED)        
        return attrs

    def validated_username(self, attrs):
        for key, value in attrs.items():
            attrs[key] = self.crypt.decrypt_text(value)
        if not User.objects.filter(
                username=attrs
        ).exists():
            raise serializers.ValidationError(detail="Login failed,User not exist!", code="auth")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ['password']


class GlobalLdapConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalLdapConfiguration
        fields = "__all__"
        # exclude = ['password']

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = "__all__"

    def make_token(self, username):
        """
        :param username:
        :return:
        """
        md5 = hashlib.md5(
            "{0}{1}{2}".format(username, str(time.time()), SECRET_KEY).encode("utf8")
        )
        return md5.hexdigest()

    def validate(self, attrs):
        attrs['token'] = self.make_token(username=attrs['username'])
        attrs['expiration_time'] = datetime.now() + datetime.timedelta(minutes=+60)
        attrs['update_date'] = datetime.now()
        return attrs

    def create(self, validated_data):
        UserToken.objects.filter(expiration_time__lte=datetime.now()).delete()
        obj = UserToken.objects.create(**validated_data)
        return obj


__all__ = [
    "SignInSerializer",
    "UserTokenSerializer",
    "UserSerializer",
    "GlobalLdapConfigurationSerializer"
]

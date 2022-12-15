from abc import ABC
import datetime
from rest_framework import serializers
from utils.crypt import AesCrypt
from devops_api.settings import SALT_KEY, SECRET_KEY
from django.contrib import auth
from apps.account.models import User, UserToken
from django.utils import timezone
import time
import hashlib


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
    crypt = AesCrypt(model='ECB', iv='', encode_='utf-8', key=SALT_KEY)

    def validate(self, attrs):
        """
        :param attrs:
        :return:
        """
        attrs['password'] = self.crypt.aesdecrypt(attrs['password'])
        if not attrs['password']:
            raise serializers.ValidationError('解码密码异常，请检查！')
        user_obj = auth.authenticate(**attrs)
        if not user_obj:
            raise serializers.ValidationError(detail="登录失败，用户名或者密码错误！{}".format(attrs), code="auth")
        User.objects.filter(**attrs).update(last_login=datetime.datetime.now())
        return attrs

    def validated_username(self, attrs):
        for key, value in attrs.items():
            attrs[key] = self.crypt.decrypt_text(value)
        if not User.objects.filter(
                username=attrs
        ).exists():
            raise serializers.ValidationError(detail="登录失败，用户不存在！", code="auth")
        return attrs


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
            "{0}{1}{2}".format(username, time.time(), SECRET_KEY).encode("utf8")
        )
        return md5.hexdigest()

    def validate(self, attrs):
        attrs['token'] = self.make_token(username=attrs['username'])
        attrs['expiration_time'] = timezone.now() + timezone.timedelta(minutes=+60)
        attrs['update_date'] = datetime.datetime.now()
        return attrs

    def create(self, validated_data):
        UserToken.objects.filter(expiration_time__lte=time.time()).delete()
        obj = UserToken.objects.create(**validated_data)
        return obj


__all__ = [
    "SignInSerializer",
    "UserTokenSerializer"
]
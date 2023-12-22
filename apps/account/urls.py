"""devops_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from apps.account.views import *

app_name = 'account'

urlpatterns = [
    path('login', UserObtainTokenPairView.as_view(), name="login"),
    path('publickey', GenericKeyView.as_view(), name="generickey"),
    path('refresh', UserObtainTokenPairView.as_view(), name="refresh"),
    re_path('users$', UserManagerView.as_view(), name="users"),
    re_path('user/(?P<pk>\d+)$', UserUpdateView.as_view(), name="user"),
    re_path('userpass$', UserPasswordUpdateView.as_view(), name="userpass"),
    re_path('userpass_check', CheckUserPasswdView.as_view(), name="userpass_check"),
    re_path('adminpass/(?P<pk>\d+)$', AdminSetPasswordUpdateView.as_view(), name="adminpass"),
    re_path('roles$', RoleManagerView.as_view(), name="roles"),
    re_path('role/(?P<pk>\d+)$', RoleUpdateView.as_view(), name="role"),
    re_path('permissions$', PermissionManagerView.as_view(), name="permissions"),
    re_path('permission/(?P<pk>\d+)$', PermissionUpdateView.as_view(), name="permission"),
    re_path('ldaps', GlobalLDAPManagerView.as_view(), name="ldaps"),
    re_path('ldap/(?P<pk>\d+)$', GlobalLDAPUpdateView.as_view(), name="ldap"),
    re_path('ldap_passwd/(?P<pk>\d+)$', GlobalLDAPPasswordUpdateView.as_view(), name="ldap_passwd")
]

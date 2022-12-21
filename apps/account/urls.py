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
# from django.contrib import admin
from django.urls import path
from apps.account.views import Login, UserManager, CurrentUser,Logout,LDAPManager

app_name = 'account'

urlpatterns = [
    path('user/login', Login.as_view(), name="login"),
    path('user/logout', Logout.as_view(), name="logout"),
    path('user/current', CurrentUser.as_view(), name="current"),
    path('user/info', UserManager.as_view(), name="info"),
    path('user/ldap', LDAPManager.as_view(), name="ldap"),
]

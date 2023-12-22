from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from apps.config.models import Projects


class Permissions(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Projects, verbose_name="所属项目", on_delete=models.CASCADE, null=True, blank=True)
    rw_permissions = models.CharField(max_length=10, blank=True, null=True, default="r", verbose_name="读写权限")
    manager = models.BooleanField(verbose_name="项目管理员", default=False)
    app_permissions = models.BooleanField(default=False, verbose_name="审核权限")

    class Meta:
        db_table = 'sys_permissions'
        # db_table_comment = '权限表'


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='角色', max_length=32, blank=False, null=False, default="default")
    permission = models.ManyToManyField(Permissions, verbose_name="项目权限")
    manager = models.BooleanField(verbose_name="系统管理员", default=False)
    desc = models.TextField(verbose_name="角色描述", blank=True)

    class Meta:
        db_table = 'sys_roles'
        # db_table_comment = "角色表"


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=50, null=False, unique=True)
    name = models.CharField(verbose_name="姓名", max_length=50, default='default')
    mobile = models.CharField(verbose_name="手机", max_length=12, null=False, default="186000000000")
    roles = models.ForeignKey(
        Role,
        verbose_name='角色',
        on_delete=models.CASCADE,
        default='',
        null=True,
        blank=True
    )
    email = models.EmailField(verbose_name="邮箱地址", unique=True, null=False)
    is_active = models.BooleanField(verbose_name="有效", default=True)
    is_staff = models.BooleanField(verbose_name="有效", default=True)
    is_superuser = models.BooleanField(verbose_name="是否是超级用户", default=True)
    create_date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True, null=True)
    update_date = models.DateTimeField(verbose_name='更新日期', auto_now_add=True, null=True)
    last_login = models.DateTimeField(verbose_name='最近登录', auto_now_add=True, null=True)
    ldap = models.BooleanField(verbose_name="是否为ldap账号", default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile', 'is_active', 'is_superuser', 'email']
    objects = UserManager()

    class Meta:
        db_table = 'sys_users'
        verbose_name_plural = "User"
        # db_table_comment = '用户表'

    def __str__(self):
        return self.username


class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="相关用户")
    login_time = models.DateTimeField(auto_now_add=True)
    ipaddress = models.GenericIPAddressField()
    logout_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sys_users_log'


class GlobalLdapConfiguration(models.Model):
    ldap_server = models.CharField(max_length=30, default="127.0.0.1:389", null=False, verbose_name="地址")
    ldap_binddn = models.CharField(max_length=80, default="default", null=False, verbose_name="监听账号")
    ldap_bindpass = models.CharField(max_length=80, default="default", null=False, verbose_name="监听密码")
    ldap_login_attribute = models.CharField(max_length=50, default="", null=False, verbose_name="登录关键字")
    ldap_base_dn = models.CharField(max_length=50, default="ou", null=False, verbose_name="登录搜索域")
    desc = models.TextField(verbose_name="备注")

    class Meta:
        db_table = 'sys_ldap'
        # db_table_comment = 'ldap配置表'


__all__ = [
    'User',
    "GlobalLdapConfiguration",
    "Role",
    "Permissions",
    "UserLog"
]

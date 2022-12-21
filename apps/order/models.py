from django.db import models


class KubernetesModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='集群名称', max_length=32, blank=False, null=False, default="default")
    address = models.CharField(verbose_name='地址', max_length=32, blank=False, null=False, default="default")
    token = models.TextField(verbose_name="认证token", blank=True)
    regular = models.TextField(verbose_name="正则信息",null=True)
    desc = models.TextField(verbose_name="备注", blank=True)

    class Meta:
        db_table = 't_kubernetes'


class KubernetesNameSpace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='名称', max_length=32, blank=False, null=False, default="default")
    kubernetes = models.ForeignKey(
        verbose_name="所属Kubernetes", null=False, on_delete=models.CASCADE, to="KubernetesModel"
    )
    namespace = models.CharField(verbose_name='命名空间', max_length=32, blank=False, null=False, default="default")
    desc = models.TextField(verbose_name="备注", blank=True)

    class Meta:
        db_table = 't_kubernetes_namespace'


class KubernetesWorkLoadServiceIngressTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(verbose_name='名称', max_length=32, blank=False, null=False, default="default")
    class_type = models.CharField(verbose_name='类型', max_length=32, blank=False, null=False, default="default")
    template = models.TextField(verbose_name="模板内容", null=False)
    desc = models.TextField(verbose_name="备注", blank=True)

    class Meta:
        db_table = 't_kubernetes_template'


class DB(models.Model):
    db_type = models.CharField(
        verbose_name="所属数据库类型",
        choices=(
            ("mysql", "mysql"),
            ("mongodb", "mongodb"),
            ("redis", "redis")
        ),
        max_length=10, default="mysql"
    )
    address = models.CharField(verbose_name="链接地址：IP:Port", max_length=50, default="127.0.0.1")
    username = models.CharField(verbose_name="用户", max_length=10, default="admin", blank=True)
    password = models.CharField(verbose_name="密码", max_length=200, default="admin", blank=True)
    uri = models.CharField(verbose_name="uri连接地址", max_length=200, default="mongo://127.0.0.1:27017")
    desc = models.TextField(verbose_name="备注")

    class Meta:
        db_table = 't_db'

class OrderNotice(models.Model):
    notice_type = models.CharField(verbose_name="通知类型",max_length=10,choices=(("wechat","企业微信"),("dingtalk","钉钉"),("email","邮件")),default='weichat')
    params = models.TextField(verbose_name="通知参数",null=False)


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    order_time = models.CharField(verbose_name='类型名称', max_length=32, blank=False, null=False, default="default")
    kubernetes = models.ForeignKey(
        verbose_name="所属Kubernetes", null=True, on_delete=models.CASCADE, to="KubernetesModel"
    )
    kubernetes_content = models.TextField(
        verbose_name="kubernetes内容", null=False
    )
    db = models.ForeignKey(
        verbose_name="所属db", null=False, on_delete=models.CASCADE, to="DB"
    )
    db_content = models.TextField(verbose_name="模板内容", null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_created=True)
    status = models.IntegerField(verbose_name="任务状态", blank=False, null=False, default=0)
    notice = models.ManyToManyField(verbose_name="通知类型",to="OrderNotice", blank=False, null=False)
    desc = models.TextField(verbose_name="备注", blank=True)

    class Meta:
        db_table = 't_orders'


__all__ = [
    'KubernetesModel',
    'KubernetesNameSpace',
    'KubernetesWorkLoadServiceIngressTemplate',
    'DB',
    'Orders'
    ]
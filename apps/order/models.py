from django.db import models
from apps.account.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    jira_order = models.CharField(
        verbose_name='jira审核订单', max_length=32, blank=False, null=False,
        default="default"
    )
    order_time = models.DateTimeField(verbose_name='类型名称', blank=False, null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_created=True, null=True, blank=True)
    status = models.IntegerField(
        verbose_name="执行状态",
        choices=((0, "还未审批"), (1, "审批中"), (2, "审批通过"), (3, "审批拒绝"),
                 (4, "审批未执行"), (5, "执行中"), (6, "执行完成"), (7, "执行失败"), (8, "任务回退中"),
                 (9, "任务回退失败"), (10, "任务取消"), (11, "任务超时")),
        default=0
    )
    notice = models.ManyToManyField(verbose_name="通知类型", to="config.Notice")
    re_orders = models.ForeignKey(verbose_name="回退工单", to="Orders", on_delete=models.CASCADE, null=True, blank=True)
    desc = models.TextField(verbose_name="发布说明", blank=True)
    order_user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=True, verbose_name="工单提交人")

    class Meta:
        db_table = 't_orders'


class SubOrders(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='suborders', null=True, blank=True)
    status = models.IntegerField(
        verbose_name="执行状态",
        choices=((0, "还未执行"), (1, "执行中"), (2, "执行成功"), (3, "执行失败")),
        default=0
    )
    service_env = models.ForeignKey(
        to='config.ServiceEnvironment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="部署服务"
    )
    images = models.ForeignKey(
        to='config.Products',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="部署镜像"
    )
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)  # 指向ContentType这个模型
    object_id = models.PositiveIntegerField()  # object_id为一个整数，存储了实例id
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )
    go_over = models.BooleanField(verbose_name="错误仍执行", default=False)
    params = models.TextField(
        verbose_name="执行参数",
        null=True,
        blank=True
    )
    correlation_name = models.CharField(verbose_name="数据库|配置文件名", max_length=100, default="default")
    is_backup = models.BooleanField(verbose_name="是否备份")
    backup_name = models.CharField(
        verbose_name="备份文件/镜像名称", max_length=200, default='default', null=True, blank=True
    )
    create_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_created=True, null=True, blank=True)
    response_user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=True, verbose_name="责任人员")

    class Meta:
        db_table = 't_suborders'


class OrderLogs(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name="订单", related_name='order_logs')
    sub_order = models.ForeignKey(SubOrders, on_delete=models.CASCADE, verbose_name="子订单")
    status = models.BooleanField(
        verbose_name="执行状态",
        default=False
    )
    logs = models.TextField(verbose_name="记录日志")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_order_logs'


__all__ = [
    'Orders',
    'SubOrders',
    'OrderLogs'
]

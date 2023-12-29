from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from utils.core.fields import AESCharField
from apps.jira.models import JiraProjectVersion


class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='名称', max_length=32, blank=False, null=False, default="default")
    git_server = models.CharField(verbose_name='配置保存地址', max_length=255, blank=True, null=True, default="default")
    git_current_commit = models.CharField(
        verbose_name="当前的commitid", max_length=255, blank=True, null=True, default=""
    )
    git_commit_time = models.DateTimeField(verbose_name="commit时间", null=True)

    class Meta:
        db_table = 't_projects'
        # db_table_comment = '项目表'


class GitCommitLog(models.Model):
    project = models.ForeignKey(Projects, verbose_name="关联项目", on_delete=models.CASCADE)
    commit_id = models.CharField(verbose_name="Commit ID", max_length=200, default="")
    commit_time = models.DateTimeField(verbose_name="commit时间")

    class Meta:
        db_table = 't_git_commits'
        # db_table_comment = '项目表'


class Environment(models.Model):
    environment = models.CharField(max_length=50, null=False, blank=False, default="开发环境", verbose_name="环境名称")
    code = models.CharField(max_length=50, null=False, blank=False, default="dev", verbose_name="环境代码")

    class Meta:
        db_table = 't_environment'
        # db_table_comment = '环境配置表'


# kubernetes 配置表
class KubernetesModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='集群名称', max_length=32, blank=False, null=False, default="default")
    kubeconfig = AESCharField(
        verbose_name='配置文件', max_length=10220, blank=False, null=False, default="default"
    )
    regular = models.TextField(verbose_name="正则信息", null=True)
    debug = models.BooleanField(default=False, verbose_name="debug", null=False)
    desc = models.TextField(verbose_name="备注", blank=True)

    class Meta:
        db_table = 't_kubernetes'
        # db_table_comment = 'kubernetes 配置表'


class SSHKey(models.Model):
    ssh_name = models.CharField(max_length=50, default="def", null=False, verbose_name="ssh名称")
    ssh_type = models.CharField(max_length=10, default="password", verbose_name="认证方式")
    ssh_username = models.CharField(max_length=50, default="default", verbose_name="用户")
    ssh_password = AESCharField(max_length=200, default="default", verbose_name="密码", null=True, blank=True)
    ssh_public_key = AESCharField(verbose_name="SSH公钥", null=True, blank=True, max_length=2000)

    class Meta:
        db_table = 't_sshkeys'
        # db_table_comment = 'SSH配置表'


class ServiceConfig(models.Model):
    service_name = models.CharField(max_length=50, verbose_name="服务名称", default="default")
    content = models.JSONField(verbose_name="文件内容")
    content_type = models.CharField(verbose_name="配置类型", max_length=15, default="config")
    description = models.TextField(verbose_name="备注")

    class Meta:
        db_table = 't_services_config'
        # db_table_comment = "服务配置表"


class Services(models.Model):
    service_name = models.CharField(max_length=50, verbose_name="服务名称", default="default", unique=True)
    service_ports_enable = models.BooleanField(verbose_name="端口启用", default=False)
    service_ports = models.JSONField(verbose_name="端口列表", default=dict)
    service_config = models.ManyToManyField(ServiceConfig, verbose_name="默认配置文件", default="default", blank=True)
    service_git = models.CharField(verbose_name="代码仓库地址", max_length=200, default="default")
    service_compile = models.CharField(verbose_name="默认编译命令", max_length=200, default="maven install")
    service_healthy_enable = models.BooleanField(verbose_name="监控启用", default=False)
    service_healthy_type = models.CharField(verbose_name="健康检查类型", max_length=200, default="tcp")
    service_readiness = models.JSONField(verbose_name="就绪探针")
    service_liveness = models.JSONField(verbose_name="存活探针")
    service_prometheus_enable = models.BooleanField(verbose_name="监控接口启用")
    service_prometheus = models.JSONField(verbose_name="监控接口")
    service_domain_enable = models.BooleanField(verbose_name="配置对外域名启用")
    service_domain = models.JSONField(verbose_name="配置对外域")
    service_skywalking_enable = models.BooleanField(verbose_name="skywalking启用")
    service_skywalking = models.JSONField(verbose_name="skywalking")

    class Meta:
        db_table = 't_services'
        # db_table_comment = "部署服务表"


class ServiceResource(models.Model):
    request_cpu = models.IntegerField(null=False, blank=False, default=100, verbose_name="需要CPU")
    request_memory = models.IntegerField(null=False, blank=False, default=500, verbose_name="需要Memory")
    limit_cpu = models.IntegerField(null=False, blank=False, default=500, verbose_name="限制CPU")
    limit_memory = models.IntegerField(null=False, blank=False, default=1000, verbose_name="限制Memory")

    class Meta:
        db_table = 't_services_resource'
        # db_table_comment = "服务资源配置"
        unique_together = (("request_cpu", "request_memory", "limit_cpu", "limit_memory"),)


class KubernetesEnvironmentConfiguration(models.Model):
    kubernetes_pull_secret = models.CharField(max_length=100, default="default", verbose_name="Harbor配置")
    kubernetes_auth = models.ForeignKey(
        KubernetesModel, on_delete=models.CASCADE, default=0, null=True, blank=True, verbose_name="关联k8s认证信息"
    )
    kubernetes_namespace = models.CharField(max_length=50, verbose_name="k8s命名空间", default="default")

    class Meta:
        db_table = 't_kubernetes_environment_configuration'
        # db_table_comment = "Kubernetes环境配置表"
        unique_together = (("kubernetes_pull_secret", "kubernetes_auth", "kubernetes_namespace"),)


class DockerEnvironmentConfiguration(models.Model):
    docker_instances = models.TextField(null=False, blank=False, default=0, verbose_name="docker部署所在主机")
    docker_ssh = models.ForeignKey(SSHKey, null=True, blank=True, verbose_name="ssh所属的KEY", on_delete=models.CASCADE)

    class Meta:
        db_table = 't_docker_environment_config'
        # db_table_comment = "Docker环境配置"
        unique_together = (("docker_instances", "docker_ssh"),)


class EnvironmentVariable(models.Model):
    config_key = models.CharField(verbose_name="环境变量Key", max_length=50, default="default")
    config_value = AESCharField(verbose_name="环境变量value", max_length=200, default="default")
    config_type = models.CharField(verbose_name="环境变量type", max_length=50, default="default")

    class Meta:
        db_table = 't_environment_variable'
        # db_table_comment = '环境变量表'
        unique_together = (("config_key", "config_value"),)


class ServiceEnvironment(models.Model):
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, verbose_name="所属环境")
    service = models.ForeignKey(
        Services, on_delete=models.CASCADE, default=0, verbose_name="关联服务", null=False, blank=False
    )
    replica_count = models.IntegerField(null=False, blank=False, default=1, verbose_name="副本数")
    resource = models.ForeignKey(ServiceResource, on_delete=models.CASCADE, null=True, blank=True, verbose_name="资源")
    service_config = models.ManyToManyField(
        ServiceConfig, verbose_name="配置文件", default="default", blank=True
    )
    environment_variable = models.ManyToManyField(
        'EnvironmentVariable', verbose_name="环境变量", default="default", blank=True
    )
    kubernetes_enable = models.BooleanField(null=False, blank=False, default=True, verbose_name="是否部署在k8s")
    kubernetes_environment_config = models.ForeignKey(
        KubernetesEnvironmentConfiguration, null=True, blank=True, verbose_name="关联k8s配置", on_delete=models.CASCADE
    )
    docker_enable = models.BooleanField(null=False, blank=False, default=False, verbose_name="是否部署在docker")
    docker_environment_config = models.ForeignKey(
        DockerEnvironmentConfiguration, null=True, blank=True, verbose_name="关联docker配置", on_delete=models.CASCADE
    )
    git_branch_or_tag = models.CharField(max_length=20, default="default", verbose_name="所用分支")
    project = models.ForeignKey("Projects", null=False, blank=False, on_delete=models.CASCADE, verbose_name="关联项目")
    auto_deploy = models.BooleanField(null=False, blank=False, default=True, verbose_name="是否自动部署")

    class Meta:
        db_table = 't_service_environment'
        # db_table_comment = "helm仓库配置表"
        unique_together = (("project", "environment", "service"),)


# helm仓库配置表
class KubernetesHelmRepoModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="仓库名称", default="default")
    helm_repo_add_command = models.CharField(verbose_name="helm repo配置命令", max_length=255, null=False)
    enable = models.BooleanField(default=False, verbose_name="是否可用")

    class Meta:
        db_table = 't_kubernetes_helm_repo'
        # db_table_comment = "helm仓库配置表"


# Helm chart 表
class KubernetesHelmChartModel(models.Model):
    id = models.AutoField(primary_key=True)
    helm_repo_chart = models.CharField(
        max_length=255, blank=False, default="deployment-repo/deployment-chart", verbose_name="helm模板")
    helm_repo = models.ForeignKey(
        to=KubernetesHelmRepoModel, blank=False, verbose_name="helm仓库", on_delete=models.PROTECT
    )
    helm_repo_chart_version = models.CharField(max_length=50, blank=False, default="0.1.3-dev")
    workload_type = models.CharField(max_length=30, blank=False, default="deployment")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    sub_order = GenericRelation(to='order.SubOrders', object_id_field='pk')

    class Meta:
        db_table = 't_kubernetes_helm'
        # db_table_comment = 'helm配置信息表'
        unique_together = (("helm_repo_chart", "helm_repo"),)


# 制品表
class Products(models.Model):
    service_environment = models.ManyToManyField(
        ServiceEnvironment,
        verbose_name="部署信息",
        blank=True
    )
    jira_version = models.ForeignKey(
        JiraProjectVersion,
        blank=True,
        null=True,
        verbose_name='所属版本',
        related_name="image_related",
        on_delete=models.CASCADE
    )
    images = models.CharField(verbose_name="镜像地址", max_length=200, null=False, blank=False, default="images")
    status = models.BooleanField(verbose_name="是否有效", null=False, default=True)
    install_status = models.BooleanField(verbose_name="是否部署", null=False, default=True)
    service = models.ForeignKey(
        Services, null=False, blank=False, on_delete=models.CASCADE,
        verbose_name="部署服务"
    )

    class Meta:
        db_table = 't_products'
        # db_table_comment = '制品表'
        unique_together = (("jira_version", "images"),)


class DB(models.Model):
    db_type = models.CharField(
        verbose_name="数据库类型",
        choices=(
            ("mysql", "mysql"),
            ("mongodb", "mongodb"),
            ("redis", "redis")
        ),
        max_length=10, default="mysql"
    )
    is_uri = models.BooleanField(verbose_name="uri格式", default=False)
    environment = models.ForeignKey(
        Environment, null=False, blank=False, on_delete=models.CASCADE, verbose_name="所属环境"
    )
    address = AESCharField(verbose_name="链接地址：IP:Port", max_length=50, default="127.0.0.1")
    username = models.CharField(verbose_name="用户", max_length=10, default="admin", blank=True)
    password = AESCharField(verbose_name="密码", max_length=200, default="admin", blank=True)
    uri = models.CharField(verbose_name="uri连接地址", max_length=200, default="mongo://127.0.0.1:27017")
    sub_order = GenericRelation(to='order.SubOrders', object_id_field='pk')
    desc = models.TextField(verbose_name="备注")

    class Meta:
        db_table = 't_db'
        unique_together = (("address", "username"),)


class Jenkins(models.Model):
    name = models.CharField(max_length=50, verbose_name="名称", default="default")
    address = AESCharField(verbose_name="链接地址：IP:Port", max_length=50, default="127.0.0.1", unique=True)

    class Meta:
        db_table = 't_jenkins'


class NaCOS(models.Model):
    address = models.CharField(max_length=50, verbose_name="nacos地址", default="default")
    protocol = models.CharField(
        max_length=50, verbose_name="访问协议", default="default", choices=(
            ("http", "http"),
            ("grpc", "grpc")
        ), )
    username = models.CharField(max_length=50, verbose_name="账号", default="default")
    password = AESCharField(max_length=100, verbose_name="密码", default="default")
    environment = models.ForeignKey(
        Environment, null=False, blank=False, on_delete=models.CASCADE, verbose_name="所属环境"
    )
    sub_order = GenericRelation(to='order.SubOrders', object_id_field='pk')

    class Meta:
        db_table = 't_nacos'
        unique_together = (("address", "username"),)


class Notice(models.Model):
    notice_type = models.CharField(
        verbose_name="通知类型", max_length=10,
        choices=(("wechat", "企业微信"), ("dingtalk", "钉钉"), ("email", "邮件")),
        default='wechat'
    )
    params = AESCharField(verbose_name="通知参数", null=False, max_length=200, unique=True)

    class Meta:
        db_table = 't_notice'


__all__ = [
    'KubernetesModel',
    'Projects',
    'DB',
    'Environment',
    'KubernetesModel',
    'SSHKey',
    'ServiceConfig',
    'Services',
    'ServiceResource',
    'KubernetesHelmRepoModel',
    'KubernetesHelmChartModel',
    'KubernetesEnvironmentConfiguration',
    'DockerEnvironmentConfiguration',
    'ServiceEnvironment',
    'Products',
    'GitCommitLog',
    'NaCOS',
    'Notice',
    'EnvironmentVariable',
    'Jenkins'
]

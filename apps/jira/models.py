from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from utils.core.fields import AESCharField


class JiraModel(models.Model):
    name = models.CharField(max_length=20, default='', verbose_name="Jira名称")
    address = models.CharField(max_length=200, default='', verbose_name="Jira地址", unique=True)
    username = models.CharField(max_length=50, default='', verbose_name="Jira账号")
    password = AESCharField(max_length=50, default='', verbose_name="Jira密码")

    class Meta:
        db_table = 't_jira'
        # db_table_comment = 'jira配置表'


class JiraProject(models.Model):
    jira = models.ForeignKey(JiraModel, related_name="jira", on_delete=models.CASCADE, verbose_name="Jira")
    project_id = models.CharField(verbose_name="jiraProject", max_length=100, default="00000000")
    project_key = models.CharField(verbose_name="项目简写", max_length=100, default="00000000")
    project_name = models.CharField(verbose_name="项目名称", max_length=200, default="00000000")
    project_description = models.TextField(verbose_name="描述", null=True, blank=True)
    project_leader = models.EmailField(verbose_name="项目负责人邮箱", null=True, blank=True)

    class Meta:
        db_table = 't_jira_project'
        # db_table_comment = 'jira项目'


class JiraProjectVersion(models.Model):
    jira_project = models.ForeignKey(JiraProject, on_delete=models.CASCADE, verbose_name="所属项目")
    project_version_id = models.CharField(verbose_name="版本ID", max_length=50, default="000000", null=True, blank=True)
    name = models.CharField(verbose_name="版本名称", max_length=10, default="default",unique=True)
    archived = models.BooleanField(verbose_name="是否归档")
    released = models.BooleanField(verbose_name="是否发布")
    start_date = models.DateTimeField(verbose_name="开始日期", null=True, blank=True)
    release_date = models.DateTimeField(verbose_name="发布日期", null=True, blank=True)
    user_start_date = models.DateField(verbose_name='研发人员开始日期', null=True, blank=True)
    users_release_date = models.DateField(verbose_name='研发人员发布日期', null=True, blank=True)

    class Meta:
        db_table = 't_jira_project_version'
        # db_table_comment = 'jira项目版本'

from rest_framework import serializers
from apps.jira.models import *
from django.utils.translation import gettext_lazy as _
from atlassian import Jira
from utils.devops_api_log import logger
import simplejson as json


class JiraModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = JiraModel
        fields = "__all__"

    def validate(self, attrs):
        from utils.core.rsa_crypt import generator
        attrs['password'] = generator.decrypt_data(data=attrs['password'])
        return attrs

    def create_project(self, data):
        serializer_data = JiraProjectSerializer(data=data, many=True)
        if not serializer_data.is_valid():
            raise serializers.ValidationError(_("Invalid project data"))
        serializer_data.save()

    def update_project(self, instance, data):
        JiraProject.objects.filter(jira=instance).delete()
        serializer_data = JiraProjectSerializer(data=data, many=True)
        if not serializer_data.is_valid():
            raise serializers.ValidationError(_("Invalid project data {}".format(serializer_data.errors)))
        serializer_data.save()

    def create(self, validated_data):
        try:
            instance = JiraModel.objects.create(**validated_data)
            jira = Jira(
                url=validated_data['address'],
                username=validated_data['username'],
                password=instance.password
            )
            instance.save()
            data = jira.get_all_projects()
            data_list = list()
            for project in data:
                temp_data = {
                    "jira": instance.id,
                    "project_id": project['id'],
                    "project_key": project['key'],
                    "project_name": project['name']
                }
                if 'projectCategory' in project.keys():
                    if 'projectCategory' in project['projectCategory'].keys():
                        temp_data['project_description'] = project['projectCategory']['description']
                data_list.append(temp_data)
            self.create_project(data=data_list)
            return instance
        except Exception as e:

            logger.error(_("Jira：Rsync failed: %s", e))
            raise serializers.ValidationError("JiraModel输入数据错误")

    def update(self, instance, validated_data):
        try:
            for key, value in validated_data.items():
                if not hasattr(instance, key):
                    continue
                setattr(instance, key, value)
            instance.save()
            jira = Jira(
                url=instance.address,
                username=validated_data['username'],
                password=validated_data['password']
            )

            data = jira.get_all_projects()
            data_list = list()
            for project in data:
                temp_data = {
                    "jira": instance.id,
                    "project_id": project['id'],
                    "project_key": project['key'],
                    "project_name": project['name']
                }
                if 'projectCategory' in project.keys():
                    if 'projectCategory' in project['projectCategory'].keys():
                        temp_data['project_description'] = project['projectCategory']['description']
                data_list.append(temp_data)
            self.update_project(instance=instance, data=data_list)
            return instance
        except Exception as e:
            logger.error(_("Jira：Rsync failed: %s", e))
            raise serializers.ValidationError("JiraModel输入数据错误")


class JiraProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = JiraProject
        fields = "__all__"


class JiraIssueField(serializers.Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        jira = Jira(
            url=value.jira_project.jira.address,
            username=value.jira_project.jira.username,
            password=value.jira_project.jira.password
        )
        jql_str = "project={} AND fixVersion={}".format(value.jira_project.project_key, value.project_version_id)
        data = jira.jql(jql=jql_str)
        logger.info("获取到的问题清单:{}".format(data))
        return data


class JiraProjectVersionSerializer(serializers.ModelSerializer):
    raw_jira_project = serializers.CharField(source="jira_project.project_name", read_only=True)
    issues = JiraIssueField(read_only=True)

    class Meta:
        model = JiraProjectVersion
        fields = "__all__"

    def create(self, validated_data):
        """
         {
    "self": "https://jira.kyoffice.cn/rest/api/2/version/11417",
    "id": "11417",
    "name": "test11",
    "archived": false,
    "released": false,
    "projectId": 10400
}
        :param validated_data:
        :return:
        """
        try:
            instance = JiraProjectVersion.objects.create(**validated_data)
            instance.save()
            jira = Jira(
                url=instance.jira_project.jira.address,
                username=instance.jira_project.jira.username,
                password=instance.jira_project.jira.password
            )
            result = jira.add_version(
                project_key=instance.jira_project.project_key,
                project_id=instance.jira_project.project_id,
                version=instance.name
            )
            instance.project_version_id = result['id']
            instance.save()
            return instance
        except Exception as e:
            JiraProjectVersion.objects.filter(**validated_data).delete()
            logger.error('Error saving project version: %s', e)
            raise serializers.ValidationError(_('Error saving project version: %s', e))

    def update(self, instance, validated_data):
        try:
            for key, value in validated_data.items():
                if not hasattr(instance, key):
                    continue
                setattr(instance, key, value)
            instance.save()
            jira = Jira(
                url=instance.jira_project.jira.address,
                username=instance.jira_project.jira.username,
                password=instance.jira_project.jira.password
            )
            result = jira.update_version(
                version=instance.project_version_id,
                is_archived=instance.archived,
                is_released=instance.released
            )
            logger.info("更新jira版本信息成功：{}".format(json.dumps(result)))
            return instance
        except Exception as e:
            JiraProjectVersion.objects.filter(**validated_data).delete()
            logger.error('Error saving project version: %s', e)
            raise serializers.ValidationError(_('Error saving project version: %s', e))


__all__ = ["JiraModelSerializer", "JiraProjectSerializer", "JiraProjectVersionSerializer"]

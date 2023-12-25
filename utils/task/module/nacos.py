import glob
import os
import re
import shutil

import nacos
import yaml
# from KubernetesManagerWeb.settings import SALT_KEY
#
# from Task.lib.Log import RecordExecLogs
# from Task.lib.base import cmd
# from Task.lib.settings import DB_BACKUP_DIR
# from Task.models import AuthKEY, ExecList, TemplateNacos
# from lib.secret import AesCrypt
from utils.task.logs import recorder
from apps.order.models import SubOrders
from apps.config.models import NaCOS
from utils.task.module import cmd

DB_BACKUP_DIR = "/data/backup"


class NacosClass:
    suborder = None

    def __init__(self):
        self.nacos = None
        self.log = None
        self.backup_dir = DB_BACKUP_DIR

    def upload_config(self, yaml_achieve, config_type):
        """
        :param yaml_achieve:
        :param config_type:
        :return:
        """
        if not os.path.exists(yaml_achieve):
            self.log.record(message="文件不存在:{}".format(yaml_achieve), status='error')
            return False
        data = yaml_achieve.split(os.path.sep)
        try:
            with open(yaml_achieve, 'r') as fff:
                load_dict = yaml.load_all(fff, Loader=yaml.Loader)
                self.nacos.publish_config(
                    content=yaml.dump_all(
                        load_dict,
                        allow_unicode=True
                    ),
                    config_type=config_type,
                    timeout=30,
                    data_id=data[-1],
                    group=data[-2]
                )
        except Exception as error:
            self.log.record(message="上传配置失败:{}".format(error), status='error')
            return False

    def connect_nacos(self, content):
        """
        :param content:
        :return:
        """
        if not isinstance(content, NaCOS):
            recorder.error(
                message="选择模板错误：{}！".format(content),
                status=3,
                suborder=self.suborder
            )
            return False
        namespace = self.suborder.correlation_name.split('.')[0]
        try:
            if content.address.endwith('443'):
                address = 'https://{}'.format(content.address)
            e:
                address = 'http://{}:{}'.format(content.auth_host, content.auth_port)
            self.nacos = nacos.NacosClient(
                address,
                namespace=namespace,
                username=content.auth_user,
                password=content.password
            )
            return True
        except Exception as error:
            # RecodeLog.error(msg="登录验证失败,{}".format(error))
            self.log.record(message="登录验证失败,{}".format(error), status='error')
            return False

    def save_context(self, sql_file, context):
        try:
            with open(sql_file, 'w') as fff:
                fff.write(context)
            recorder.info(
                suborder=self.suborder,
                message='success to save sql file:{}'.format(sql_file),
                status=2
            )
            return True
        except Exception as e:
            recorder.error(
                suborder=self.suborder,
                message='Failed to write sql file:{}'.format(e),
                status=3
            )
            return False

    def run(self, suborder: SubOrders):
        """
        :param suborder:
        :return:
        """
        self.suborder = suborder
        db_name = suborder.correlation_name
        suborder_obj = suborder.content_object
        suborder_content = suborder.params
        suborder_content_file = "nacos-{}-{}.yaml".format(suborder.id, db_name)
        suborder_content_file = os.path.join(DB_BACKUP_DIR, suborder_content_file)
        if not self.save_context(sql_file=suborder_content_file, context=suborder_content):
            return False

        if not self.connect_nacos(
                suborder_obj
        ):
            return False
        name, extension = os.path.splitext(suborder_content_file)
        if extension != '.yaml':
            recorder.error(
                message="文件类型错误:{}".format(suborder_content_file),
                status=3,
                suborder=self.suborder
            )
            return False
        if not self.upload_config(yaml_achieve=suborder_content_file, config_type="yaml"):
            return False

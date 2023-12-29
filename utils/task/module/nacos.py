import glob
import os

import nacos
import yaml
from utils.task.logs import recorder
from apps.order.models import SubOrders
from apps.config.models import NaCOS

DB_BACKUP_DIR = "/data/backup"


class NacosClass:
    suborder = None

    def __init__(self):
        self.nacos = None
        self.log = None
        self.backup_dir = DB_BACKUP_DIR

    def upload_config(self, config_type):
        """
        :param config_type:
        :return:
        """
        data = self.suborder.correlation_name.split('.')
        try:
            self.nacos.publish_config(
                content=yaml.dump_all(
                    self.suborder.params,
                    allow_unicode=True
                ),
                config_type=config_type,
                timeout=30,
                data_id=data[1],
                group=data[2]
            )
            return True
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
            else:
                address = 'http://{}:{}'.format(content.address.split(':')[0], content.address.split(':')[1])
            self.nacos = nacos.NacosClient(
                address,
                namespace=namespace,
                username=content.username,
                password=content.password
            )
            return True
        except Exception as error:
            recorder.error(
                message="NaCOS登录验证失败,{}".format(error),
                status=3,
                suborder=self.suborder
            )
            return False

    def run(self, suborder: SubOrders):
        """
        :param suborder:
        :return:
        """
        self.suborder = suborder
        suborder_obj = suborder.content_object

        if not self.connect_nacos(
                suborder_obj
        ):
            return False
        if not self.upload_config(config_type="yaml"):
            return False

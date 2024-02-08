import time

from django.core.management.base import BaseCommand
from apps.config.models import ServiceEnvironment, Products
from utils.devops_api_log import logger
from utils.core.harbor import HarborSDKManager
# from jenkins import Jenkins
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class Command(BaseCommand):
    hb = HarborSDKManager()

    def handle(self, *args, **options):
        while True:
            self.run_task()
            time.sleep(10)

    def run_task(self):
        for data in ServiceEnvironment.objects.all():
            logger.info("获取到配置信息: 命名空间=>{},服务名称:{}".format(
                data.kubernetes_environment_config.kubernetes_namespace, data.service.service_name
            ))
            logger.info("获取到配置信息: 账号=>{},地址=>{}".format(
                data.project.harbor_username, data.project.harbor_domain
            ))
            self.hb.connect(
                username=data.project.harbor_username,
                password=data.project.harbor_password,
                host=data.project.harbor_domain
            )
            data_artifacts = self.get_artifacts(
                namespace=data.kubernetes_environment_config.kubernetes_namespace,
                service_name=data.service.service_name
            )
            data_product = Products.objects.values("images")
            data_product = [x['images'] for x in data_product]
            add = set(data_artifacts).difference(set(data_product))
            if add:
                logger.info("发现新镜像:{}".format(add))
            product_list = list()
            for x in add:
                product_list.append(
                    Products(service=data.service, images=x, status=1, publish=0)
                )
            Products.objects.bulk_create(product_list, batch_size=2000)

    def get_artifacts(self, namespace, service_name, page=1, repository_image_list=list()):
        logger.info("Getting artifacts from {},service: {},page {}".format(namespace, service_name, page))
        try:
            repository_list = self.hb.get_artifacts(
                project_name=namespace,
                repository_name=service_name,
                page_size=100,
                page=page
            )
            if not repository_list:
                raise ValueError("不存在数据")
            for x in repository_list:
                repository = ["harbor.newtsp.newcowin.com/{}/{}:{}".format(
                    namespace, service_name, y.name
                ) for y in x.tags]
                repository_image_list.extend(repository)
            return self.get_artifacts(namespace, service_name, page + 1, repository_image_list)
        except ValueError:
            logger.info("翻页查询完毕")
            return repository_image_list
        except Exception as e:
            logger.error("查询异常:{}".format(e))
            return repository_image_list

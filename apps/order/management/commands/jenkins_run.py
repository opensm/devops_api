import time

from django.core.management.base import BaseCommand
from apps.order.models import JenkinsOrders
from utils.devops_api_log import logger
from jenkins import Jenkins
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class Command(BaseCommand):
    SUB_TASK_STATUS = 0

    def handle(self, *args, **options):
        while True:
            self.run_bonded_threads()

    def run_task(self):
        for data in JenkinsOrders.objects.filter(
                status=0
        ):
            if not self.check_task_status(
                    order=data
            ):
                continue
            logger.info("Jenkins status: 开始任务：{}".format(data.jenkins_order_id))
            self.run_jenkins(order=data)
            time.sleep(5)

    def update_task_status(self):
        for data in JenkinsOrders.objects.filter(
                status__lt=2
        ):
            self.update_task(order=data)

    def run_bonded_threads(self, max_threads=None):
        if self.SUB_TASK_STATUS == 1:
            return
        self.SUB_TASK_STATUS = 1

        thread_list = list()
        if not max_threads:
            pool = ThreadPoolExecutor()
        else:
            pool = ThreadPoolExecutor(max_workers=max_threads)
        with pool as th:
            t_sub = th.submit(self.run_task)
            thread_list.append(t_sub)
            t_sub = th.submit(self.update_task_status)
            thread_list.append(t_sub)
        # 逐步校验执行结果
        for t in as_completed(thread_list):
            if not t.result():
                self.SUB_TASK_STATUS = 0
                return False
        self.SUB_TASK_STATUS = 0
        return True

    @staticmethod
    def check_task_status(order: JenkinsOrders):
        """
        :param order:
        :param :
        :return:
        """
        # jk = Jenkins(
        #     order.jenkins.address,
        #     username=order.order_user.username,
        #     password=order.order_user.password
        # )
        jk = Jenkins(
            order.jenkins.address,
            username='yaoshaoqiang',
            password='w9vM7BQoED6fg.uheO'
        )
        job_info = jk.get_job_info(name=order.jenkins.name)
        job_list = [x['number'] for x in job_info['builds']]
        if order.jenkins_order_id in job_list:
            return False
        else:
            return True

    @staticmethod
    def update_task(order: JenkinsOrders):
        """
        :param order:
        :param :
        :return:
        """
        jk = Jenkins(
            order.jenkins.address,
            username='yaoshaoqiang',
            password='w9vM7BQoED6fg.uheO'
        )
        job_info = jk.get_job_info(name=order.jenkins.name)
        job_list = [x['number'] for x in job_info['builds']]
        logger.info("获取到的Jenkins任务清单：{}".format(job_list))
        logger.info("当前的任务ID：{}".format(order.jenkins_order_id))
        if order.jenkins_order_id in job_list:
            order_build_info = jk.get_build_info(name=order.jenkins.name, number=order.jenkins_order_id)
            output = jk.get_build_console_output(name=order.jenkins.name, number=order.jenkins_order_id)
            logger.info("{}：编译信息，{}".format(order.jenkins_order_id, order_build_info))
            order.jenkins_queue_id = order_build_info['queueId']
            order.output = output
            logger.info("当前任务是否在运行：{}".format(order_build_info['inProgress']))
            if order_build_info['inProgress']:
                order.status = 1
                logger.info("Order build inProgress {}".format(order.jenkins_order_id))
            else:
                if order_build_info['result'] == 'SUCCESS':
                    logger.info("Order build SUCCESS {}".format(order.jenkins_order_id))
                    order.status = 2
                    order.duration = order_build_info['duration']
                    order.order_time = datetime.fromtimestamp(order_build_info['timestamp'] / 1000)
                elif order_build_info['result'] == 'FAILURE':
                    logger.info("Order build FAILURE {}".format(order.jenkins_order_id))
                    order.duration = order_build_info['duration']
                    order.order_time = datetime.fromtimestamp(order_build_info['timestamp'] / 1000)
                    order.status = 3
                elif order_build_info['result'] == 'ABORTED':
                    logger.info("Order build ABORTED {}".format(order.jenkins_order_id))
                    order.status = 4
                else:
                    logger.info("Order build UnKnow {}".format(order.jenkins_order_id))
                    order.status = 5
            order.save()
            return False
        else:
            order.status = 1
            return True

    def get_task_parameters(self, order: JenkinsOrders):
        parameters = dict()
        data = order.service_env
        env = data.environment.code
        project = data.kubernetes_environment_config.kubernetes_namespace
        branch = data.git_branch_or_tag
        repo_url = data.service.service_git
        build_params = data.service.service_build_params
        build_path = data.service.service_build_path
        service_name = data.service.service_name
        build_type = data.service.service_type
        build_bin = data.service.service_build_bin
        parameters['branch_name'] = branch
        parameters['repo_url'] = repo_url
        parameters['build_params'] = build_params
        parameters['build_path'] = build_path
        parameters['project_name'] = project
        parameters['env'] = env
        parameters['service_name'] = service_name
        parameters['build_type'] = build_type
        parameters['build_bin'] = build_bin
        return parameters

    def run_jenkins(self, order: JenkinsOrders):
        """
        :param order:
        :return:
        """
        # jk = Jenkins(
        #     order.jenkins.address,
        #     username=order.order_user.username,
        #     password=order.order_user.password
        # )
        jk = Jenkins(
            order.jenkins.address,
            username='yaoshaoqiang',
            password='w9vM7BQoED6fg.uheO'
        )
        params = self.get_task_parameters(order=order)
        try:
            jk.build_job(name=order.jenkins.name, parameters=params)
            return True
        except Exception as e:
            logger.error("任务执行错误：{}:{}".format(order.jenkins.name, e))
            return False

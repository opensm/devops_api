
from __future__ import print_function
import kubernetes.client
from kubernetes import client,utils
from kubernetes.client.rest import ApiException
from apps.order.models import KubernetesModel, Orders
from datetime import timedelta, timezone, datetime
import time,os,yaml
import simplejson as json
from devops_api.settings import SALT_KEY
from utils.crypt import AesCrypt
from utils.exceptions import *


class KubernetesClass:
    def __init__(self):
        self.configuration = client.Configuration()
        self._api = None
        self._log = None
        self.limit_time = int(time.time()) - 300
        # self._notification = NoticeSender()
    
    def set_configuration(self, obj: KubernetesModel):
        """
        :param obj:
        :return:
        """
        crypt = AesCrypt(model='ECB', iv='', encode_='utf-8', key=SALT_KEY)
        auth_key = crypt.aesdecrypt(obj.token)
        if not auth_key:
            raise ParamErrorException(message='Invalid auth key')
        self.configuration.api_key = {"authorization": "Bearer {}".format(auth_key)}
        self.configuration.verify_ssl = False
        self.configuration.debug = False
        if not obj.address.startswith('https://'):
            self.configuration.host = 'https://' + obj.address
        elif obj.address.startswith('http://'):
            raise ParamErrorException(message='http:// is not allowed')
        else:
            self.configuration.host = obj.address
    
    def connect(self,obj: KubernetesModel, api_type="CoreV1Api"):
        """
        :param obj:
        :param api_type: CoreV1Api,AppsV1Api
        :return:
        """
        try:
            # 初始化configuration
            self.set_configuration(obj=obj)
            api_client = kubernetes.client.ApiClient(self.configuration)
            _api = getattr(kubernetes.client,api_type)
            self._api =_api(api_client)
            print("认证成功!")
        except Exception as error:
            # self._log.record(message="认证异常！{}".format(error))
            print("认证异常！{}".format(error))
            raise PermissionDeniedException(message="kubernetes login is not allowed")

    def list_namespaced_resources(
        self, 
        namespace:str, 
        api_class:str, 
        resource:str,
        **kwargs,
        ):
        """
        :param namespace:
        :param api_class: CoreV1Api,AppsV1Api
        :param resource: deployment,stateful_set,daemon_set,cron_job,service,config_map,secret
        :param kwargs field_selector=None,label_selector=None,timeout_seconds=600,limit=100,pretty=True
        """
        if not hasattr(self._api,api_class):
            raise DataNotExistException(message="API class not found!")
        if not hasattr(self._api,"list_{}_for_all_namespaces".format(resource)):
            raise DataNotExistException(message="Resource not found!")
        _api_resource = getattr(self._api,"list_{}_for_all_namespaces".format(resource))
        request_kwargs= dict()
        for key, value in kwargs.items():
            if value:
                request_kwargs[key] = value
        res = _api_resource(namespace=namespace,**request_kwargs)        
        return res
    
    def list_namespace(self,pretty=True,**kwargs):
        """
        :return:
        """
        print(self._api)
        request_kwargs = dict()
        for key, value in kwargs.items():
            if value:
                request_kwargs[key] = value
            else:
                continue
        res = self.list_namespace(pretty=pretty,**request_kwargs)
        return res
    
    def read_namespaced_resource(self,namespace,resource,name,pretty=True):
        """
        read_namespaced_resource
        :param namespace:
        :param resource: deployment,stateful_set,daemon_set,cron_job,service,config_map,secret
        """
        if not hasattr(self._api,"read_namespaced_{}".format(resource)):
            raise DataNotExistException(message="Resource not found!")
        _api_resource = getattr(self._api,"read_namespaced_{}".format(resource))
        res = _api_resource(namespace=namespace,name=name,pretty=pretty)
        return res
    
    def patch_namespaced_resource(
        self,
        resource,
        namespace,
        name,
        body,
        **kwargs
        ):
        """
        patch_namespaced_resource
        :param resource: deployment,stateful_set,daemon_set,cron_job,service
        :param namespace:
        :param name:
        :param body:
        :param kwargs pretty=False,dry_run=True, field_manager=None, field_validation=None, force=False
        """
        if not hasattr(self._api,"patch_namespaced_{}".format(resource)):
            raise DataNotExistException(message="Resource not found!")
        _api_resource = getattr(self._api,"patch_namespaced_{}".format(resource))
        request_kwargs= dict()
        for key, value in kwargs.items():
            if value:
                request_kwargs[key] = value
        res = _api_resource(namespace=namespace,name=name,body=body,**request_kwargs)
        return res

    def get_namespace_from_yaml(self,yaml_file):
        """
        :param yaml_file:
        :return namespace:
        """
        if not os.path.exists(yaml_file):
            raise DataNotExistException(message="File %s does not exist".format(yaml_file))
        try:
            with open(yaml_file, 'r') as fff:
                datas = yaml.load(fff,Loader=yaml.FullLoader)
            if 'metadata' not in datas.keys():
                raise DataNotExistException(message="File %s does not contain metadata".format(yaml_file))
            if 'namespace' not in datas['metadata'].keys():
                raise DataNotExistException(message="File %s does not contain namespace".format(yaml_file))
            if not datas['metadata']['namespace']:
                raise DataNotExistException(message="File %s does contain namespace error".format(yaml_file))
            return datas['metadata']['namespace']
        except yaml.YAMLError as exc:
            pm = exc.problem_mark
            raise ContentErrorException(message="{} has an issue on line {} at position {}".format(pm.name, pm.line, pm.column))
        except Exception as error:
            raise ContentErrorException(message="File %s content Error: %s" % (yaml_file, error))
    
    def check_yaml_content(self,resource_type:str, content:dict):
        """
        check_yaml_content
        :param resource_type:
        :param content:
        :return:
        """
        pass
        
        

    def apply_resource_from_yaml(self,yaml_file):
        """
        :param yaml_file:
        :param namespace:
        :return Bool: True if
        """
        namespace = self.get_namespace_from_yaml(yaml_file=yaml_file)
        res = utils.create_from_yaml(self.configuration,yaml_file,namespace=namespace,verbose=True)
        if not res: return False
        else: return True
    
    def retry_run_function(self, function, kwargs, times=5):
        if times <= 0:
            self._log.record(
                status='error',
                message="函数:{},调用异常:{},尝试次数用完退出！".format(
                    function, times
                )
            )
            return None
        try:
            return function(**kwargs)
        except Exception as error:
            time.sleep(1)
            times = times - 1
            self._log.record(
                status='error',
                message="函数:{},调用异常:{},还剩{}次尝试！".format(
                    function, error, times
                )
            )
            return self.retry_run_function(
                function=function,
                kwargs=kwargs,
                times=times
            )
    
    def get_deployments(self,namespace):
        return self.api_core.list_namespaced_deployment(
            namespace=namespace,
            label_selector="app=kubedl"
        )

    def get_deployment(self, deployment_name, namespace):
        """
        :param deployment_name:
        :param namespace:
        :return:
        """
        kwargs = {
            "name": deployment_name,
            "namespace": namespace,
            "pretty": "true",
            "exact": True,
            "export": True
        }
        function = getattr(self.api_apps, 'read_namespaced_deployment')
        result = self.retry_run_function(function=function, kwargs=kwargs)
        if not result:
            self._log.record(message="获取delployment失败!")
        return result

    def check_deploy_image(self, deployment, name, exec_list):
        """
        :param deployment:
        :param name:
        :param exec_list:
        :return:
        """
        if not isinstance(exec_list, ExecList):
            raise TypeError("输入任务类型错误！")
        containers = deployment.spec.template.spec.containers
        for i in range(len(containers)):
            if containers[i].name != name:
                continue
            else:
                if containers[i].image != exec_list.params:
                    return False
                else:
                    self._log.record(message="更新镜像与在线镜像一致，跳过更新!".format(containers[i].image))
                    return True
        return False

    def update_deployment(self, namespace, deployment, name, exec_list):
        """
        :param namespace:
        :param deployment:
        :param name:
        :param exec_list:
        :return:
        """
        if not isinstance(exec_list, ExecList):
            raise TypeError("输入任务类型错误！")
        containers = deployment.spec.template.spec.containers
        for i in range(len(containers)):
            if containers[i].name != name:
                continue
            else:
                try:
                    exec_list.output = containers[i].image
                    exec_list.save()
                    self._log.record(message="保存老镜像成功:{}".format(containers[i].image))
                except Exception as error:
                    self._log.record(message="保存老镜像失败:{}".format(error))
                    return False
                containers[i].image = exec_list.params
                deployment.spec.template.spec.containers = containers

        kwargs = {
            "namespace": namespace,
            "name": name,
            "body": deployment
        }
        function = getattr(self.api_apps, 'patch_namespaced_deployment')
        result = self.retry_run_function(function=function, kwargs=kwargs)
        if not result:
            self._log.record(message="更新镜像失败!")
        return result
        # try:
        #     self.api_apps.patch_namespaced_deployment(
        #         namespace=namespace,
        #         name=name,
        #         body=deployment
        #     )
        #     return True
        # except ApiException as e:
        #     self.log.record(message="更新镜像失败: %s\n" % e)
        #     return False

    def check_pods_status(self, namespace, name, label, count=30, replicas=0):
        """
        :param namespace:
        :param name:
        :param label:
        :param count:
        :param replicas
        :return:
        """
        result = True
        self._log.record(message="还剩：{}次尝试次数!".format(count))
        after = self.get_deployment_pods(
            namespace=namespace,
            name=name,
            label=label,
            limit_time=self.limit_time
        )
        self._log.record("获取POD个数:{}".format(after))
        count = count - 1
        if len(after) < replicas and count > 0:
            self._log.record(message="启动pod数不够，现：{}".format(after))
            time.sleep(10)
            return self.check_pods_status(
                namespace=namespace,
                name=name,
                label=label,
                count=count,
                replicas=replicas
            )
        elif len(after) < replicas and count == 0:
            self._log.record(message="检测超时:{}".format(name))
            return False
        else:
            for x in after:
                kwargs = {
                    "namespace": namespace,
                    "name": x
                }
                function = getattr(self.api_core, 'read_namespaced_pod_status')
                status = self.retry_run_function(function=function, kwargs=kwargs)
                if not status:
                    self._log.record(message="更新镜像失败!")
                    continue
                # status = self.api_core.read_namespaced_pod_status(namespace=namespace, name=x)
                for a in status.status.container_statuses:
                    if not a.ready:
                        result = False
                if not result and count > 0:
                    self._log.record(message="启动pod:{},状态不正确，等待10s，即将下次检测!".format(x))
                    time.sleep(10)
                    return self.check_pods_status(
                        namespace=namespace,
                        name=name,
                        label=label,
                        count=count,
                        replicas=replicas
                    )
                elif not result and count == 0:
                    self._log.record(message="启动pod状态不正确，检测超时，任务失败!")
                    return False
                else:
                    return True

    def get_deployment_pods(self, namespace, name, label, limit_time=None):
        """
        :param namespace:
        :param name:
        :param label:
        :param limit_time:
        :return:
        """
        kwargs = {
            "namespace": namespace,
            "label_selector": label.format(name)
        }
        function = getattr(self.api_core, 'list_namespaced_pod')
        data = self.retry_run_function(function=function, kwargs=kwargs)
        # data = self.api_core.list_namespaced_pod(
        #     namespace=namespace,
        #     label_selector=label.format(name)
        # )
        if not data:
            self._log.record(message="更新镜像失败!")
            return False
        if not limit_time:
            return [x.metadata.name for x in data.items]
        else:
            return [
                x.metadata.name for x in data.items
                if int(time.mktime(
                    x.metadata.creation_timestamp.astimezone(timezone(timedelta(hours=8))).timetuple()
                )) >= limit_time
            ]

    def check_pod_logs(self, pod, namespace):
        """
        :param pod:
        :param namespace:
        :return:
        """
        compare = False
        error_str = ""
        kwargs = {
            "namespace": namespace,
            "name": pod
        }
        function = getattr(self.api_core, 'read_namespaced_pod_log')
        data = self.retry_run_function(function=function, kwargs=kwargs)
        if not data:
            self._log.record(message="更新镜像失败!")
            return ''
        # data = self.api_core.read_namespaced_pod_log(name=pod, namespace=namespace)
        for line in data.split('\n'):
            for key in POD_CHECK_KEYS:
                if key in line:
                    compare = True
                if line.startswith(str(datetime.now().year)):
                    compare = False
            if compare:
                error_str = "{}\n{}".format(error_str, line)
        return error_str

    def update(self, exec_list, logs):
        if not isinstance(exec_list, ExecList):
            raise TypeError("输入任务类型错误！")
        if not isinstance(logs, RecordExecLogs):
            raise TypeError("输入任务类型错误！")

        self._log = logs
        template = exec_list.content_object

        if not isinstance(template, TemplateKubernetes):
            self._log.record(message="传入模板类型错误!")
            return False
        if not self.connect_apps(obj=template.cluster):
            self._log.record(message="链接K8S集群失败!")
            return False

        deployment = self.get_deployment(
            deployment_name=template.app_name,
            namespace=template.namespace
        )
        if not deployment:
            self._log.record(message="获取deployment失败!")
            return False

        if self.check_deploy_image(
                deployment=deployment,
                name=template.app_name,
                exec_list=exec_list
        ):
            return True

        if not self.update_deployment(
                deployment=deployment,
                name=template.app_name,
                namespace=template.namespace,
                exec_list=exec_list
        ):
            self._log.record(message="镜像发布失败：{}".format(exec_list.params))
            return False
        else:
            time.sleep(20)
            if not self.check_pods_status(
                    namespace=template.namespace,
                    name=template.app_name,
                    label=template.label,
                    count=30,
                    replicas=deployment.spec.replicas
            ):
                self._log.record(message="镜像发布失败，容器状态不正确：{}！".format(exec_list.params))
                return False

            pods = self.get_deployment_pods(
                namespace=template.namespace,
                name=template.app_name,
                label=template.label,
                limit_time=self.limit_time
            )
            for x in pods:
                msg = self.check_pod_logs(pod=x, namespace=template.namespace)
                if msg:
                    message = "### >报错容器: {} \n### >报错信息:{}\n".format(x, msg)
                    title = "发版信息：{} {}".format(self._log.project.name, self._log.task.name)
                    user_list = [
                        self._log.task.create_user.mobile,
                        self._log.sub_task.create_user.mobile
                    ]
                    self._notification.sender_file(
                        title=title, msg=message, mentioned=user_list, is_all=False
                    )
        self._log.record(message="镜像发布成功：{}！".format(exec_list.params))
        return True

    def restart(self, exec_list, logs):
        if not isinstance(exec_list, ExecList):
            raise TypeError("输入任务类型错误！")
        if not isinstance(logs, RecordExecLogs):
            raise TypeError("输入任务类型错误！")
        self._log = logs
        template = exec_list.content_object
        if not isinstance(template, TemplateKubernetes):
            self._log.record(message="传入模板类型错误!")
            return False
        if not self.connect_apps(obj=template.cluster):
            self._log.record(message="链接K8S集群失败!")
            return False
        deployment = self.get_deployment(
            deployment_name=template.app_name,
            namespace=template.namespace
        )
        if not deployment:
            self._log.record(message="获取deployment失败!")
            return False
        try:
            now = datetime.utcnow()
            now = str(now.isoformat("T") + "Z")
            body = {
                'spec': {
                    'template': {
                        'metadata': {
                            'annotations': {
                                'kubectl.kubernetes.io/restartedAt': now
                            }
                        }
                    }
                }
            }

            kwargs = {
                "namespace": template.namespace,
                "name": template.app_name,
                "body": body,
                "pretty": 'true'
            }
            function = getattr(self.api_apps, 'patch_namespaced_deployment')
            data = self.retry_run_function(function=function, kwargs=kwargs)
            if not data:
                self._log.record(message="更新镜像失败!")
                return False
            # self.api_apps.patch_namespaced_deployment(
            #     namespace=template.namespace,
            #     name=template.app_name,
            #     body=body,
            #     pretty='true'
            # )
            time.sleep(20)
            if not self.check_pods_status(
                    namespace=template.namespace,
                    name=template.app_name,
                    label=template.label,
                    count=20,
                    replicas=deployment.spec.replicas
            ):
                self._log.record(message="镜像发布失败，容器状态不正确：{}！".format(exec_list.params))
                return False
            pods = self.get_deployment_pods(
                namespace=template.namespace,
                name=template.app_name,
                label=template.label,
                limit_time=self.limit_time
            )
            for x in pods:
                msg = self.check_pod_logs(pod=x, namespace=template.namespace)
                if msg:
                    message = "### >报错容器: {} \n### >报错信息:{}\n".format(x, msg)
                    title = "发版信息：{} {}".format(self._log.project.name, self._log.task.name)
                    user_list = [
                        self._log.task.create_user.mobile,
                        self._log.sub_task.create_user.mobile
                    ]
                    self._notification.sender_file(
                        title=title, msg=message, mentioned=user_list, is_all=False
                    )
            self._log.record(message="重启操作成功：{}！".format(exec_list.params))
            return True
        except ApiException as e:
            self._log.record(message="重启deployment失败，原因: %s\n" % e)
            return False
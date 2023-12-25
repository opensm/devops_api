from django.core.management.base import BaseCommand
from apps.order.models import Orders, SubOrders
import time, datetime
from utils.task.logs import recorder
from utils.task.multi import MultiSubTask
from utils.task import module as class_import


class Command(BaseCommand):
    t_subtask = MultiSubTask()

    def handle(self, *args, **options):
        while True:
            for data in Orders.objects.filter(
                    status=2
            ):
                if not self.check_task_status(task=data):
                    continue
                recorder.info(msg='即将开始任务:{}:{}'.format(
                    data.id,
                    data.desc
                ))
                if not self.run_task(task=data):
                    message = "任务失败,任务ID:{},任务内容:{}".format(
                        data.id,
                        data.desc
                    )
                    recorder.failed(
                        status='失败',
                        title="任务ID:{}".format(data.id),
                        message=message,
                        task_time=data.task_time,
                        finish_time=data.finish_time
                    )
                else:
                    massage = '任务完成,任务ID:{},任务内容：{}'.format(data.id, data.desc)
                    recorder.success(
                        status=0,
                        title="{}-{}".format(data.id, data.name),
                        message=massage,
                        task_time=data.task_time,
                        finish_time=data.finish_time
                    )

    @staticmethod
    def check_task_status(task):
        """
        :param task:
        :return:
        """
        local_time = time.time()
        task_unixtime = datetime.datetime.strptime(
            task.task_time,
            "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        if not isinstance(task, Orders):
            raise TypeError('任务类型错误！')
        if task_unixtime > local_time:
            return False
        elif (local_time - task_unixtime) > 60 * 20:
            task.status = 11
            task.save()
            return False
        elif task_unixtime < local_time and task.status != 2:
            return False
        elif task_unixtime < local_time and task.status == 2:
            return True

    def run_task(self, task: Orders):
        if not isinstance(task, Orders):
            raise TypeError('任务类型错误！')
        task.status = 5
        task.save()
        for sub in SubOrders.objects.filter(order=task):
            exec_type = sub.content_object
            if sub.content_type.model == 'db':
                exec_class_name = "{}Class".format(exec_type.db_type.capitalize())
                exec_class = getattr(class_import, exec_class_name)
            else:
                exec_class_name = "{}Class".format(sub.content_type.model)
                exec_class = getattr(class_import, exec_class_name)

            if not exec_class.run():
                if not sub.force():
                    sub.status = False
                    sub.save()
                    task.status = 7
                    task.save()
                    return False
            sub.status = True
            sub.save()
        task.status = 6
        task.save()
        return True

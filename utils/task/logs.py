from utils.devops_api_log import logger
from apps.order.models import OrderLogs, SubOrders
from utils.task.notice import NoticeSender


class Recorder(object):
    logger = logger
    model = OrderLogs
    notice = NoticeSender()

    def info(self, suborder: SubOrders, status: int, message: str):
        self.recording(suborder=suborder, status=status, logs=message)
        self.logger.info(msg=message)

    def error(self, suborder: SubOrders, status: int, message: str):
        self.recording(suborder=suborder, status=status, logs=message)
        self.logger.error(msg=message)

    def warning(self, suborder: SubOrders, status: int, message: str):
        self.recording(suborder=suborder, status=status, logs=message)
        self.logger.warning(msg=message)

    def debug(self, suborder: SubOrders, status: int, message: str):
        self.recording(suborder=suborder, status=status, logs=message)
        self.logger.debug(msg=message)

    @staticmethod
    def recording(suborder: SubOrders, status: int, logs: str):
        OrderLogs.objects.create(order=suborder.order, suborder=suborder, status=status, logs=logs)
        return

    def failed(self, suborder: SubOrders, status: int, message: str):
        mention_list = list()
        mention_list.append(suborder.order.order_user.mobile)
        mention_list.append(suborder.response_user.mobile)
        self.error(suborder=suborder, status=status, message=message)
        self.notice.get_sender_config(notice_data=suborder.order.notice.all())
        self.notice.sender(title="运维系统通知信息", msg=message, mentioned=mention_list)

    def success(self, suborder: SubOrders, status: int, message: str):
        mention_list = list()
        mention_list.append(suborder.order.order_user.mobile)
        mention_list.append(suborder.response_user.mobile)
        self.info(suborder=suborder, status=status, message=message)
        self.notice.get_sender_config(notice_data=suborder.order.notice.all())
        self.notice.sender(title="运维系统通知信息", msg=message, mentioned=mention_list)


recorder = Recorder()

__all__ = ['recorder']

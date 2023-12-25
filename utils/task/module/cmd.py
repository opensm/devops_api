from utils.devops_api_log import logger
import platform


def cmd(cmd_str, replace=''):
    """
    :param cmd_str:
    :param replace:
    :return:
    """
    if int(platform.python_version().strip(".")[0]) < 3:
        import commands
        exec_proc = commands
    else:
        import subprocess
        exec_proc = subprocess
    try:
        status, output = exec_proc.getstatusoutput(cmd_str)
        if status != 0:
            raise Exception(output)
        if not replace:
            msg = "执行:{0},成功!".format(cmd_str)
        else:
            msg = "执行:{0},成功!".format(cmd_str).replace(replace, '********')
        logger.info(message=msg)
        return True
    except Exception as error:
        if not replace:
            msg = "执行:{0},失败，原因:{1}".format(cmd_str, error)
        else:
            msg = "执行:{0},失败，原因:{1}".format(cmd_str, error).replace(replace, '********')
        logger.error(message=msg)
        return False

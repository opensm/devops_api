# -*- coding: utf-8 -*-
import pymysql
import os
import datetime
# from Task.lib.settings import DB_BACKUP_DIR
# from Task.lib.Log import RecordExecLogs
# from Task.lib.base import cmd
# from Task.models import AuthKEY, TemplateDB, ExecList
# from KubernetesManagerWeb.settings import SALT_KEY
# from lib.secret import AesCrypt
from apps.order.models import SubOrders
from utils.task.logs import recorder
from apps.config.models import DB
from utils.task.module import cmd

DB_BACKUP_DIR = "/data/backup"


class MySQLClass:
    suborder = None

    def __init__(self):
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.log = None
        self.backup_dir = DB_BACKUP_DIR
        self.auth_str = None
        self.cursor = None
        self.auth_dump_str = None
        if not os.path.exists(self.backup_dir):
            raise Exception(
                "{0} 不存在！".format(self.backup_dir)
            )
        if not os.path.exists("/usr/bin/mysql") or not os.path.exists("/usr/bin/mysqldump"):
            raise Exception("mysql或者mysqldump 没找到可执行程序！")

    def check_db(self, db):
        self.cursor.execute("show databases like '{0}';".format(db))
        res = self.cursor.fetchall()
        if len(res):
            return True
        else:
            # RecodeLog.error(msg="数据库：{0},不存在！")
            self.log.record(message="数据库：{0},不存在！", status='error')
            return False

    def backup_all(self):
        cmd_str = "/usr/bin/mysqldump {0} --all-databases|gzip >{1}".format(
            self.auth_str,
            os.path.join(
                self.backup_dir,
                "{0}-{1}-{2}-all-database.gz".format(
                    self.host, self.port, datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                )
            )

        )
        cmd(cmd_str=cmd_str, replace=self.password)

    def backup_one(self, db, achieve):
        if not self.check_db(db=db):
            return False
        cmd_str = "/usr/bin/mysqldump {0} {1}|gzip >{2}".format(
            self.auth_str,
            db,
            os.path.join(
                self.backup_dir,
                "{}.gz".format(achieve)
            )
        )
        if not cmd(cmd_str=cmd_str, replace=self.password):
            return False
        return True

    def exec_sql(self, db, sql):
        """
        :param db:
        :param sql:
        :return:
        """
        if not os.path.exists(
                os.path.join(self.backup_dir, sql)
        ):
            raise Exception("文件不存在：{0}".format(os.path.join(self.backup_dir, sql)))
        filename, filetype = os.path.splitext(sql)
        if filetype == ".sql":
            cmd_str = "/usr/bin/mysql {0} {1} < {2}".format(
                self.auth_str,
                db,
                os.path.join(self.backup_dir, sql)
            )
        elif filetype == ".gz":
            cmd_str = "zcat {2}|/usr/bin/mysql {0} {1}".format(
                self.auth_str,
                db,
                os.path.join(self.backup_dir, sql)
            )
        else:
            recorder.error(message="不能识别的文件类型:{}".format(sql), status=3, suborder=self.suborder)
            return False

        if not cmd(cmd_str=cmd_str, replace=self.password):
            recorder.error(
                message="导入数据失败:{}！".format(cmd_str).replace(self.password, '********'),
                status=3,
                suborder=self.suborder
            )
            # recover_str = "zcat {2}.gz|/usr/bin/mysql {0} {1}".format(
            #     self.auth_str,
            #     db,
            #     os.path.join(self.backup_dir, filename)
            # )
            # if not cmd(cmd_str=recover_str, replace=self.password, logs=self.log):
            #     self.log.record(
            #         message="回档数据失败:{}，请手动处理！".format(recover_str).replace(self.password, '********'),
            #         status='error'
            #     )
            # else:
            #     self.log.record(
            #         message="回档数据成功:{}！".format(recover_str).replace(self.password, '********')
            #     )
            # return False
        else:
            recorder.info(
                message="导入数据成功:{}".format(cmd_str).replace(self.password, '********'),
                suborder=self.suborder,
                status=2
            )
            return True

    def connect_mysql(self, content):
        """
        :param content:
        :return:
        """
        if not isinstance(content, DB):
            self.log.record(message="选择模板错误：{}！".format(content), status='error')
            return False
        # crypt = AesCrypt(model='ECB', iv='', encode_='utf-8', key=SALT_KEY)
        # self.password = crypt.aesdecrypt(content.auth_passwd)
        # if not self.password:
        #     self.log.record(message='解密密码失败，请检查！', status='error')
        #     return False
        auth_dict = {
            "user": content.username,
            "password": content.password,
            "host": content.address.split(":")[0],
            "port": content.address.split(":")[1],
            "database": self.suborder.correlation_name
        }
        try:
            self.password = content.password
            conn = pymysql.connect(
                connect_timeout=10,
                charset='utf8',
                **auth_dict
            )
            self.cursor = conn.cursor()
        except Exception as error:
            recorder.error(
                message="MySQL登录验证失败,{}".format(error),
                status=3,
                order=self.suborder.order,
                suborder=self.suborder
            )
            return False
        self.auth_str = "-h{host} -P{port} -u{usr} -p{password} --default-character-set=utf8 ".format(**auth_dict)
        return True

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
        suborder_content_file = "mysql-{}-{}.sql".format(suborder.id, db_name)
        suborder_content_file = os.path.join(DB_BACKUP_DIR, suborder_content_file)

        if not self.save_context(sql_file=suborder_content_file, context=suborder_content):
            return False
        if not self.connect_mysql(suborder_obj):
            return False
        filename, filetype = os.path.splitext(suborder_content_file)
        if suborder.is_backup:
            if not self.backup_one(
                    db=db_name,
                    achieve=filename
            ):
                return False
            try:
                suborder.backup_name = "{}.gz".format(filename)
                suborder.save()
                recorder.info(
                    message="保存备份数据情况成功:{}!".format("{}.gz".format(filename)),
                    suborder=self.suborder,
                    status=2
                )
                return True
            except Exception as error:
                recorder.error(
                    message="保存备份数据情况失败:{}!".format(error),
                    suborder=self.suborder,
                    status=3
                )
                return False
        if not self.exec_sql(sql=suborder_content_file, db=db_name):
            return False


__all__ = [
    'MySQLClass'
]

# -*- coding: utf-8 -*-
import pymongo
import datetime
import os
from utils.task.logs import recorder
from utils.task.module import cmd
from apps.order.models import SubOrders
from apps.config.models import DB

DB_BACKUP_DIR = "/data/db_backup"


class MongoClass:
    suborder = None

    def __init__(self):
        self.password = None
        self.auth_str = None
        self.log = None
        if not os.path.exists(DB_BACKUP_DIR):
            raise Exception(
                "{0} 不存在！".format(DB_BACKUP_DIR)
            )
        if not os.path.exists("/usr/bin/mongodump") or not os.path.exists("/usr/bin/mongorestore"):
            raise Exception("mongo或者mongodump, mongorestore没找到可执行程序！")
        self.conn = None

    def check_db(self, db):
        res = self.conn.list_database_names()
        if db in res:
            return True
        else:
            self.log.record(message="数据库：{0},不存在！".format(db))
            return False

    def backup_all(self, host, port):
        cmd_str = "/usr/bin/mongodump {0} --forceTableScan --gzip --archive={1}".format(
            self.auth_str,
            os.path.join(
                DB_BACKUP_DIR,
                "mongo-{0}-{1}-{2}-all-database.gz".format(
                    host, port, datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                )
            )
        )
        cmd(cmd_str=cmd_str, replace=self.password)

    def backup_one(self, db, achieve):
        if not self.check_db(db=db):
            return
        cmd_str = "/usr/bin/mongodump {0} -d {1} --forceTableScan --gzip --archive={2}".format(
            self.auth_str,
            db,
            os.path.join(
                DB_BACKUP_DIR,
                "{}.gz".format(achieve)
            )
        )
        if not cmd(cmd_str=cmd_str, replace=self.password):
            return False
        else:
            return True

    def exec_sql(self, db, sql):
        """
        :param db:
        :param sql:
        :return:
        """
        if not os.path.exists(
                os.path.join(DB_BACKUP_DIR, sql)
        ):
            raise Exception("文件不存在：{0}".format(os.path.join(DB_BACKUP_DIR, sql)))
        filename, filetype = os.path.splitext(sql)
        if filetype == ".js":
            cmd_str = "/usr/bin/mongo {0} {1}  {2}".format(
                self.auth_str,
                db,
                os.path.join(DB_BACKUP_DIR, sql)
            )
        elif filetype == ".gz":
            cmd_str = "zcat {2}|/usr/bin/mongorestore {0} {1} --archive".format(
                self.auth_str,
                db,
                os.path.join(DB_BACKUP_DIR, sql)
            )
        else:
            recorder.error(
                message="不能识别的文件类型:{}".format(sql),
                status=3,
                
                suborder=self.suborder
            )
            return False
        if not cmd(cmd_str=cmd_str, replace=self.password):
            recorder.error(
                message="导入数据失败:{}".format(cmd_str).replace(self.password, '********'),
                status=3,  suborder=self.suborder
            )
            # 自动回档功能注释掉
            # recover_str = "zcat {2}|/usr/bin/mongorestore {0} {1} --archive".format(
            #     self.auth_str,
            #     db,
            #     os.path.join(DB_BACKUP_DIR, filename)
            # )
            # if not cmd(cmd_str=recover_str, replace=self.password):
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

    def connect(self, content):
        """
        :param content:
        :return:
        """
        if not isinstance(content, DB):
            recorder.error(
                message="获取执行类型错误：{}！".format(content),
                status=3,
                
                suborder=self.suborder
            )
            return False
        if content.is_uri:
            self.auth_str = content.uri
            pymongo.MongoClient()
        else:
            self.password = content.password
            self.auth_str = "mongo://{}:{}:{}:{}/{}?authSource=admin".format(
                content.username,
                content.password,
                content.address.split(":")[0],
                content.address.split(":")[1],
                self.suborder.correlation_name
            )
        try:
            self.conn = pymongo.MongoClient(host=self.auth_str)
        except Exception as error:
            recorder.error(message="Mongodb登录验证失败,{}".format(error), status=3, suborder=self.suborder)
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
        suborder_content_file = "mongo-{}-{}.js".format(suborder.id, db_name)
        suborder_content_file = os.path.join(DB_BACKUP_DIR, suborder_content_file)

        if not self.save_context(sql_file=suborder_content_file, context=suborder_content):
            return False
        if not self.connect(suborder_obj):
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
                recorder.info(message="保存备份数据情况成功:{}!".format("{}.gz".format(filename)))
                return True
            except Exception as error:
                recorder.error(message="保存备份数据情况失败:{}!".format(error))
                return False
        if not self.exec_sql(sql=suborder_content_file, db=db_name):
            return False


__all__ = [
    'MongoClass'
]

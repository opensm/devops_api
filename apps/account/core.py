# -*- coding: utf-8 -*-
# !/usr/bin/env python
from ldap3 import Tls
from ldap3 import Server, Connection, ALL, NTLM, MODIFY_REPLACE, extend
import os, datetime
from utils.devops_api_log import logger

"""
@Author: yaoshaoqiang
@Description: AD域
@Date: 2018-12-23 21:23:57
@LastEditTime: 2019-03-28 23:46:56
"""


class Adopter:
    """
    操作AD域的类
    """

    def __init__(
            self,
            domain,
            ip,
            ca_certs_file,
            ca_certs_path,
            pwd=None,
            user='administrator'
    ):
        """
        domain: 域名，格式为：xxx.xxx.xxx
        ip： ip地址，格式为：192.168.214.1
        user： 管理员账号
        pwd： 管理员密码
        """
        self.domain = domain
        self.DC = ','.join(['DC=' + dc for dc in domain.split('.')])  # csc.com -> DC=csc,DC=com
        self.pre = domain.split('.')[0].upper()  # 用户登陆的前缀
        self.ip = ip
        self.admin = user
        self.pwd = pwd

        tls_configuration = Tls(
            # validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1,
            ca_certs_file=ca_certs_file,
            ca_certs_path=ca_certs_path
        )
        self.server = Server(self.ip, get_info=ALL, use_ssl=True, tls=tls_configuration)
        self.conn = Connection(
            self.server,
            user=self.pre + '\\' + self.admin,
            password=self.pwd,
            auto_bind=True,
            authentication=NTLM
        )

    def search(self, org):
        """
        查询组织下的用户
        org: 组织，格式为：aaa.bbb 即bbb组织下的aaa组织，不包含域地址
        """
        att_list = [
            'displayName',
            'userPrincipalName',
            'userAccountControl',
            'sAMAccountName',
            'pwdLastSet',
            'member',
            'mail',
            'objectClass'
        ]

        org_base = ','.join(['OU=' + ou for ou in org.split('.')]) + ',' + self.DC
        res = self.conn.search(
            search_base=org_base,
            search_filter='(objectclass=user)',  # 查询数据的类型
            attributes=att_list,  # 查询数据的哪些属性
            paged_size=1000
        )  # 一次查询多少数据
        if res:
            for user_name in self.conn.entries:
                yield user_name
        else:
            logger.error('查询失败:{} '.format(self.conn.result['description']))
            raise Exception("查询异常")

    def get_expiring_soon_user(self, org, expire):
        users = self.search(org=org)
        user_dict = dict()
        if users:
            for user in users:  # 遍历查询结果
                if str(user['userAccountControl']) != "544" and str(user['userAccountControl']) != "512":
                    continue
                last_time = str(user['pwdLastSet'])  # 将最后一次更改密码时间的数据类型转换为字符串型
                last_time = last_time[0:last_time.find('.')]  # 去掉最后一次更改密码时间后的无关字符串
                last_time = last_time[0:last_time.find('+')]  # 去掉最后一次更改密码时间后的无关字符串
                last_time = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')  # 更改数据类型为时间
                # if (datetime.datetime.now() - last_time).days >= 83 and (datetime.datetime.now() - last_time).days <= 91:  # 筛选7天内密码即将过期以及密码已经过期一天的用户
                if (datetime.datetime.now() - last_time).days >= (expire - 7):  # 筛选7天内密码即将过期以及密码已经过期一天的用户
                    temp = dict()
                    temp['expireTime'] = expire - (datetime.datetime.now() - last_time).days
                    temp['mail'] = str(user['mail'])
                    temp['displayName'] = str(user['displayName'])
                    temp['pwdLastSet'] = str(user['pwdLastSet'])
                    temp['sAMAccountName'] = str(user['sAMAccountName'])
                    # temp['mail'] = 'yaoshaoqiang@newcowin.com'
                    user_dict[str(user['sAMAccountName'])] = temp  # 将这些用户放入字典中（邮箱为key，上一次更改密码的时间为value）

        else:
            logger.error('查询失败: ', self.conn.result['description'])
        return user_dict

    def get_nomal_user(self, org):
        users = self.search(org=org)
        user_dict = dict()
        if users:
            for user in users:  # 遍历查询结果
                if str(user['userAccountControl']) != "544" and str(user['userAccountControl']) != "512":
                    continue
                user_dict[str(user['sAMAccountName'])] = user

        else:
            logger('查询失败: ', self.conn.result['description'])
        return user_dict

    def add_org(self, org):
        """
        增加组织
        org: 组织，格式为：aaa.bbb 即bbb组织下的aaa组织，不包含域地址
        """
        org_base = ','.join(['OU=' + ou for ou in org.split('.')]) + ',' + self.DC
        res = self.conn.add(org_base, object_class='OrganizationalUnit')  # 成功返回True，失败返回False
        if res:
            logger.info('增加组织[ {} ]成功！'.format(org))
        else:
            logger.error('增加组织[ {} ]发生错误" '.format(self.conn.result['description']))

    def modify_user(self, *args, **kwargs):
        """
        修改用户
        params: kwargs
        """
        org = kwargs.pop('org')
        org_base = ','.join(['OU=' + ou for ou in org.split('.')]) + ',' + self.DC
        kwargs['userPrincipalName'] = kwargs['mail']
        kwargs['userAccountControl'] = "544"
        kwargs['mobile'] = kwargs['mobile'].replace('\n', '')
        kwargs['pwdLastSet'] = -1
        self.modify_ad_user(basedn='CN={},{}'.format(kwargs['sAMAccountName'], org_base), configs=kwargs)

    def disable_user(self, *args, **kwargs):
        """
        修改用户
        params: kwargs
        """
        org = kwargs.pop('org')
        org_base = ','.join(['OU=' + ou for ou in org.split('.')]) + ',' + self.DC
        kwargs['userAccountControl'] = "514"
        self.modify_ad_user(basedn='CN={},{}'.format(kwargs['sAMAccountName'], org_base), configs=kwargs)

    def add_user(
            self,
            org,
            displayName,
            sAMAccountName,
            cn,
            mail,
            title,
            department,
            sn,
            userAccountControl,
            mobile
    ):
        """
        增加用户
        params: org增加到该组织下
        params: name：显示名称
        params: uid：账号
        params: departmentName
        params: sAMAccountType
        """
        org_base = ','.join(['OU=' + ou for ou in org.split('.')]) + ',' + self.DC
        user_att = {
            'mail': mail,
            'cn': cn,
            'displayName': displayName,
            'userPrincipalName': mail,  # uid@admin组成登录名
            'userAccountControl': userAccountControl,  # 启用账号
            'sAMAccountName': sAMAccountName,
            'department': department,
            'pwdLastSet': -1,  # 取消下次登录需要修改密码
            'sn': sn,
            'mobile': mobile,
            # 'userPassword': 'P@ssw0rd',
            'title': title
        }
        res = self.conn.add(
            'CN={},{}'.format(sAMAccountName, org_base),
            object_class=['top', 'organizationalPerson', 'person', 'user'],
            attributes=user_att
        )
        if res:
            logger.info('增加用户[ {} ]成功！开始生效用户！'.format(displayName))
            if self.set_password(config='CN={},{}'.format(sAMAccountName, org_base)):
                self.enable_ad_user(config='CN={},{}'.format(sAMAccountName, org_base))
        else:
            logger.error('增加用户[ {} ]发生错误：{}'.format(
                self.conn.result['description'],
                self.conn.result['message'])
            )

    def set_password(self, config):
        try:
            res = self.conn.extend.microsoft.modify_password(
                config,
                new_password="P@ssw0rd",
                old_password=""
            )
            if not res:
                raise Exception(res['message'])
            logger.info("设置密码{}成功！".format(config))
            return True
        except Exception as error:
            logger.error("设置密码{}错误：{},即将删除用户！".format(config, error))
            self.delete_ad_user(config=config)
            return False

    def modify_ad_user(self, basedn, configs: dict):
        """
        """
        user_config = dict()
        for key, value in configs.items():
            if isinstance(value, list):
                user_config[key] = [(MODIFY_REPLACE, value)]
            else:
                user_config[key] = [(MODIFY_REPLACE, [value])]

        if user_config:
            self.conn.modify(dn=basedn, changes=user_config)
            logger.info("修改用户信息为：{}".format(user_config))
        else:
            logger.error("获取到用户信息错误，停止修改")

    def enable_ad_user(self, config):
        """ 启用ad用户 :param username: :param adconfig: :return: """
        try:
            logger.info("enable_ad_user :" + config)
            self.conn.modify(
                config,
                {'userAccountControl': [(MODIFY_REPLACE, ['544'])]}
            )
            res = self.conn.result
            if res['result'] != 0 or res['description'] != 'success':
                raise Exception(res['description'])
            logger.info("生效用户成功:{}！".format(config))
            return True
        except Exception as e:
            logger.error("生效用户失败：{},{}".format(config, e))
            return False

    def delete_ad_user(self, config):
        """ 删除ad用户 :param username: :param adconfig: :return: """
        try:
            logger.info("delete_ad_user :" + config)
            res = self.conn.delete(config)
            logger.info("删除用户成功：{}".format(res))
            return res
        except Exception as e:
            logger.error("delete_ad_user error: %s", e)
            return False


__all__ = ['Adopter']

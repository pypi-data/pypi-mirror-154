#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import mysql.connector
from mysql.connector import errorcode
from zhufo_tools.logger import MyLogger
from dbutils.pooled_db import PooledDB


mysql_log = MyLogger("mysql_log", level=20).logger


class PyMysql:

    # 构造函数
    def __init__(self, connect_pool_config: dict, cursor_type=False):
        """
             :param cursor_type: 返回类型是否为dict
             :param connect_pool_config: 连接池配置信息
             :return: 连接成功返回数据库句柄，失败返回None
             """
        self.cursor_type = cursor_type
        self.mysql_pool = PooledDB(mysql.connector, maxconnections=connect_pool_config['db_max_num'], blocking=True, **connect_pool_config['db_config'])

    # 打开一个连接
    @staticmethod
    def sql_open(db_config, max_retry: int = 50, time_delay: int = 10):
        """
        :param db_config:
        :param max_retry: 最大重试连接次数50次
        :param time_delay: 每次链接延时10s
        :return: 连接成功返回数据库句柄，失败返回None
        """
        handle = None
        for rec in range(max_retry):
            try:
                handle = mysql.connector.connect(**db_config)
                break
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    mysql_log.info("something is wrong with you user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    mysql_log.info("database does not exist")
                else:
                    mysql_log.info("mysql init err=[{0}]".format(err))
            except Exception as err:
                mysql_log.error(f"unknown error when connecting to db, error: {err}")
            time.sleep(time_delay)
        return handle

    # 使用连接池打开数据库
    def sql_open_pool(self, max_retry: int = 50, time_delay: int = 10):
        """
        :param max_retry: 最大重试连接次数50次
        :param time_delay: 每次链接延时10s
        :return: 连接成功返回数据库句柄，失败返回None
        """
        handle = None
        for rec in range(max_retry):
            try:
                handle = self.mysql_pool.connection()
                break
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    mysql_log.info("something is wrong with you user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    mysql_log.info("database does not exist")
                else:
                    mysql_log.info("mysql init err=[{0}]".format(err))
            except Exception as err:
                mysql_log.error(f"unknown error when connecting to db, error: {err}")
            time.sleep(time_delay)

        return handle

    # 关闭数据库连接
    @staticmethod
    def sql_close(handle):
        handle.close()

    # mysql转义函数
    @staticmethod
    def escape(value):
        if isinstance(value, (bytes, bytearray)):
            value = value.replace(b"\\", b"\\\\")
            value = value.replace(b"\n", b"\\n")
            value = value.replace(b"\r", b"\\r")
            value = value.replace(b"\047", b"\134\047")  # single quotes
            value = value.replace(b"\042", b"\134\042")  # double quotes
            value = value.replace(b"\032", b"\134\032")  # for Win32
        if isinstance(value, str):
            value = value.replace("\\", "\\\\")
            value = value.replace("\n", "\\n")
            value = value.replace("\r", "\\r")
            value = value.replace("\047", "\134\047")  # single quotes
            value = value.replace("\042", "\134\042")  # double quotes
            value = value.replace("\032", "\134\032")  # for Win32
        return value

    # 查询数据库命令
    def select_mysql_record(self, handle, select_all_cmd=""):
        """
        :param handle: 句柄
        :param select_all_cmd: sql
        :return: 成功返回 {} json
                 失败返回 None
        """
        info = None
        cnt = 10
        while cnt > 0:
            cursor = handle.cursor(dictionary=self.cursor_type)
            try:
                cursor.execute("SET NAMES utf8mb4")
                cursor.execute(select_all_cmd)
                info = cursor.fetchall()
            except mysql.connector.Error as err:
                mysql_log.info("Something went wrong: {0}".format(err))
                mysql_log.info("mysql err select_cmd={0}".format(select_all_cmd))
                time.sleep(1)
                cnt -= 1
                continue
            break

        return info

    def sql_in_str(self, items: list, _char="'"):
        """构造sql , 链接格式"""
        return ", ".join(map(lambda x: f"{_char}{self.escape(x)}{_char}", items))

    def insert_or_update_mysql_record_many(
            self,
            handle,
            db_table: str,
            list_values: list,
            hope_update_list=[],
            is_ignore=False
    ):
        """
        批量插入或批量更新数据库---字典形式
        :param handle: 句柄
        :param db_table: 表名
        :param list_values: 包含字段字典的列表
        :param hope_update_list: 主键冲突时，希望更新的字段列表
        :param is_ignore: 等于True表示主键相同,不进行插入操作。 默认为False
        :return : 成功返回 > 1的 rowcount
                  失败返回 -1
        """

        row_count = -1  # 影响的条数
        cnt = 3
        while cnt > 0:
            cursor = handle.cursor()
            if not isinstance(list_values, list):
                raise ValueError("list_values must be a list!")

            # 将list_values转为sql语句
            str_temp = ""
            str_key = ""
            for values in list_values:
                if str_key == "":
                    str_key = self.sql_in_str([k for k in values.keys()], _char="")
                str_temp += "(" + self.sql_in_str([v for v in values.values()]) + ")" + " ,"
            str_temp = str_temp[:-1]  # 去最后一个逗号

            if hope_update_list:
                hope_update = ""
                for key_tmp in hope_update_list:
                    hope_update += key_tmp + "=" + "VALUES({0})".format(key_tmp)
                    hope_update += ","
                hope_update = hope_update[:-1]

                insert_cmd = "INSERT INTO {0} ({1}) VALUES {2} ON DUPLICATE KEY UPDATE {3}".format(
                    db_table, str_key, str_temp, hope_update
                )
            else:
                insert_cmd = "INSERT INTO {0} ({1}) VALUES {2}".format(
                    db_table, str_key, str_temp
                )

            # 如果is_ignore 为 True,表示主键相同,不进行插入操作
            if is_ignore:
                insert_cmd = "INSERT ignore INTO {0} ({1}) VALUES {2} ".format(
                    db_table, str_key, str_temp
                )

            try:
                cursor.execute("SET NAMES utf8mb4")
                cursor.execute(insert_cmd)
                handle.commit()
            except mysql.connector.Error as err:
                mysql_log.info("Something went wrong: {0}".format(err))
                mysql_log.info("mysql err insert_cmd={0}".format(insert_cmd))

                time.sleep(1)
                cnt -= 1
                continue
            else:
                row_count = cursor.rowcount
                break

        return row_count

    @staticmethod
    def execute_cmd(self, handle, execute_sql=""):
        row_count = -1
        cnt = 10
        while cnt > 0:
            cursor = handle.cursor()
            try:
                cursor.execute(execute_sql)
                handle.commit()
            except mysql.connector.Error as err:
                mysql_log.info("Something went wrong: {0}".format(err))
                mysql_log.info("mysql err select_cmd={0}".format(execute_sql))
                time.sleep(1)
                cnt -= 1
                continue
            else:
                row_count = cursor.rowcount
                break
        return row_count


def mysql_test():
    db_config = {
        "db_max_num": 20,  # 最大连接数
        "db_config": {
            "host": "",
            "user": "",
            "password": "",
            "port": 3306,
            "database": "",
            "charset": "utf8",
        }
    }
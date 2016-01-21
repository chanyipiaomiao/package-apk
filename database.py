#!/usr/bin/env python
# coding=utf-8

import sys
import mysql.connector as mysql
from mysql.connector import errorcode


# 定义数据库IP、用户名、密码
db_setting = {
    'host': '10.10.10.125',
    'user': 'xxxx',
    'password': 'xxx',
    'database': 'xxxx',
    'raise_on_warnings': True
}

# 查询 平台assemble_name 语句
select_assemble_name_sql = """
    SELECT assemble_name FROM mobile_android_platform_info;
"""


# 插入 渠道发布 语句
insert_channel_deploy_sql = """
INSERT INTO mobile_android_channel_deploy_info
  (channel_name,platform,assemble_name,channel,app_name,package_link,
    need_replace_ico,version,apk_dir,package_svn_number,package_date_time)
VALUES
  (%(channel_name)s,%(platform)s,%(assemble_name)s,%(channel)s,%(app_name)s,
    %(package_link)s,%(need_replace_ico)s,%(version)s,%(date)s,%(package_svn_number)s,%(package_date_time)s);
"""


# 连接Mysql
def conn_mysql():
    try:
        connection = mysql.connect(**db_setting)
    except mysql.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        sys.exit(1)
    return connection


# 管理连接和游标
def manage_connection_cursor():
    conn = conn_mysql()
    cursor = None
    if conn.is_connected():
        cursor = conn.cursor()
    return conn, cursor

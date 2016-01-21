#!/usr/bin/env python
# coding=utf-8

import os
import time
import datetime
import common
import sys
import database
import warnings


# svn 代码那块有个警告,在这里忽略
warnings.filterwarnings('ignore')


# excel文件的路径
excel_file = 'android.xlsx'


# 读取excel文件 判断 excel文件中的 assemble_name 是否在 数据库中 不存在就退出程序
package_dict, apk_number = common.read_excel(excel_file)

if not package_dict:
    print "Not Found apk need package,exit."
    time.sleep(2)
    sys.exit(0)

# 连接数据库 查询数据库中的assemble_name
connection, cursor = database.manage_connection_cursor()
cursor.execute(database.select_assemble_name_sql)
assemble_name_list_in_db = [assemble_name[0] for assemble_name in cursor]

for assemble_name_in_excel in package_dict.keys():
    if assemble_name_in_excel not in assemble_name_list_in_db:
        print "sheet name setting error"
        sys.exit(1)


# 开始打包apk文件 当excel表格中 new_package 列是 yes 的情况下才打包
start_time = datetime.datetime.now()

# 根目录
root_dir = 'D:/deploy/AndroidStudio-Project/native5.0_pro'

# 得到当前目录的SVN版本号
wc_svn_number = common.get_wc_svn_number(root_dir)

# 生成的apk目录
apk_root = '%s/apk/%s' % (root_dir, common.get_date())

# 项目目录
project_root = '%s/ivp50_pro' % root_dir
os.chdir(project_root)


# 开始打包apk
print
print "---------------------------"
print " Found  %s apk need package" % apk_number
print "---------------------------"


for assemble_name, every_platform_channel_list in package_dict.iteritems():
    for channel_package_info_dict in every_platform_channel_list:
        channel_package_info_dict['package_date_time'] = common.get_date_time()
        channel_package_info_dict['platform'] = assemble_name.lower()
        channel_package_info_dict['date'] = common.get_date()
        channel_package_info_dict['assemble_name'] = assemble_name
        channel_package_info_dict['package_svn_number'] = wc_svn_number
        cmd = common.command_str % channel_package_info_dict
        cursor.execute(database.insert_channel_deploy_sql, channel_package_info_dict)
        os.system(cmd.encode('gbk'))

# 提交
connection.commit()


# 输出执行时间
end_time = datetime.datetime.now()
print
print "--------------------------"
print " %s apk , Total Time: %s s" % (apk_number, (end_time - start_time).seconds)
print "--------------------------"


# 关闭游标和数据库连接
cursor.close()
connection.close()


# 打包 mapping目录里面的文件为zip包
os.chdir(project_root + '/build/outputs')
common.zip_files(common.get_dir_file_list('./mapping'), apk_root + '/mapping_%s.zip' % common.get_date_time2())
sys.exit(0)

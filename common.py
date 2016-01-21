#!/usr/bin/env python
# coding=utf-8

import os
import sys
import zipfile
import svn.local
from time import strftime
from openpyxl import load_workbook


def get_date():
    return strftime('%Y%m%d')


def get_date_time():
    return strftime('%Y-%m-%d %H:%M:%S')


def get_date_time2():
    return strftime('%Y-%m-%d_%H%M%S')


def get_dir_file_list(path):
    file_list = []
    for path, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            full_path = os.path.join(path, file_name)
            file_list.append(full_path)
    return file_list


def zip_files(files_list, zip_name):
    zf = zipfile.ZipFile(zip_name, 'w', zipfile.zlib.DEFLATED)
    for i in files_list:
        zf.write(i)
    zf.close()


def get_input(prompt):
    return raw_input(prompt).strip()


def get_wc_svn_number(path):
    os.chdir(path)
    wc_info = svn.local.LocalClient('.')
    return wc_info.info()['commit#revision']


def read_excel(filename):
    wb = load_workbook(filename=filename, read_only=True)
    all_sheets_names = wb.get_sheet_names()
    result_dict = {}
    apk_number = 0
    for sheet_name in all_sheets_names:
        sheet_all_rows = wb.get_sheet_by_name(sheet_name).rows
        try:
            first_row = sheet_all_rows.next()
        except StopIteration:
            print 'sheet content error'
            sys.exit(1)
        first_row_list = [first.value for first in first_row]
        result_dict[sheet_name] = []
        for row_tuple in sheet_all_rows:
            temp_dict = {}
            for key, cell in zip(first_row_list, row_tuple):
                temp_dict[key] = cell.value
            if temp_dict['new_package'] in ['yes', 'YES', 'Yes', 'YEs']:
                result_dict[sheet_name].append(temp_dict)

    # 字典中找出空的值
    null_list = []
    for key, value in result_dict.iteritems():
        if value:
            apk_number += len(value)
        else:
            null_list.append(key)

    # 字典删除空的值
    for i in null_list:
        del result_dict[i]

    return result_dict, apk_number


command_str = u"gradle -Dorg.gradle.project.channel=%(channel)s " \
          u"-Dorg.gradle.project.platform=%(platform)s " \
          u"-Dorg.gradle.project.versionName=%(version)s " \
          u"-Dorg.gradle.project.appName=%(app_name)s " \
          u"-Dorg.gradle.project.packageLink=%(package_link)s " \
          u"-Dorg.gradle.project.replace=%(need_replace_ico)s " \
          u"-Ddate=%(date)s clean assemble%(assemble_name)sRelease".encode('gbk')

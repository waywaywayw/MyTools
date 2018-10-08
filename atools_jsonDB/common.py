# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-06
"""

import os, re
import json


class MyJsonDB(object):
    def __init__(self, db_path):
        """
        初始化数据库，初始化res列表
        :param db_path:
        """
        # 没找到数据库文件
        if not os.path.isfile(db_path):
            print('数据库地址不存在，已新建数据库数据')
            open(db_path, 'w', encoding='utf8').close()

        # self._db_name = db_name
        self._db_path = db_path
        self._resource_list = self.load_from_db(db_path)
        pass

    def is_duplicate(self, key_name, resource, res_db=None):
        """
        判重
        :param res: 需要判重的数据
        :param res_db: 资源数据库
        :param key_name: 判重的关键key的name
        :return:
        """
        if not res_db:
            res_db = self._resource_list

        # resource里没有key_name属性的情况
        if not resource.get(key_name):
            return False

        ret = False
        for r in res_db:
            # print(r)
            # print(r[key_name])
            if resource[key_name] == r[key_name]:
                ret = True
        return ret

    def load_from_db(self, db_path, encoding='utf8'):
        """
        从db中读取resource_list
        :return:
        """
        resource_list = []
        with open(db_path, 'r', encoding=encoding) as fin:
            for line in fin:
                res = json.loads(line.strip())
                resource_list.append(res)
        return resource_list

    def write_to_db(self, save_path=None, resource_list=None, write_mode='w', encoding='utf8', verbose=False):
        """
        将json列表格式的resource_list写入db, 遇到重复的自动不添加
        :param db_path:
        :param resource_list:
        :return: 写入成功，返回True
        """
        if not save_path:
            save_path = self._db_path
        if not resource_list:
            resource_list = self._resource_list
        # 写入数据库
        with open(save_path, write_mode, encoding=encoding) as db_file:
            for res in resource_list:
                # 有中文需要：ensure_ascii=False
                res_json = json.dumps(res, ensure_ascii=False, sort_keys=True)
                # 实际写入
                db_file.write(res_json + '\n')
                if verbose:
                    print(res_json)
        return True

    # resource_list的get, set方法
    def get_resource_list(self):
        return self._resource_list

    def set_resource_list(self, resource_list):
        self._resource_list = resource_list

    def extend_resource_list(self, resource_list):
        """扩展resource_list, 参数为resource of list"""
        self._resource_list.extend(resource_list)
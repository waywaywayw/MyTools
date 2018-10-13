# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-29
"""
import re
import pytest


def dereplicate(elems, key=None):
    """删除重复元素，并保证元素顺序不变。支持普通类型和特殊类型(dict)的list
    """
    if key is None: # 普通hash类型，比较简单
        ret_elems = list(set(elems))
        ret_elems.sort(key=elems.index)

    else:   # 不可hash类型，比如dict类型
        ret_elems = []  # 用于存储去重结果
        duplicate_elems = set() # 用于判重
        for elem in elems:
            val = elem if key is None else key(elem)
            if val not in duplicate_elems:
                ret_elems.append(elem)
                duplicate_elems.add(val)
    return ret_elems

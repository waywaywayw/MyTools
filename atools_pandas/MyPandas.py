# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018/10/13
"""
import os
import re
import numpy as np
import pandas as pd


def drop_rows(source, func, inplace=False):
    """
    针对一行数据，如果一行数据中的某些项满足给定条件，就删除该行。
    目前使用source.iterrows遍历数据，效率较慢。。
    :param source: 需要处理的DataFrame
    :param func: 说明给定条件。满足条件时返回True。
    :param inplace: 是否就地删除。
    :return: 处理好的source
    """
    need_del_rows = []
    for idx, row in source.iterrows():
        if func(row):
            need_del_rows.append(idx)
    source = source.drop(need_del_rows, inplace=inplace)
    return source


if __name__ == "__main__":
    pass

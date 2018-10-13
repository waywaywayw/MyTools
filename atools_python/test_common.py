# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018/10/13
"""
import os
import re
import pytest
import numpy as np
import pandas as pd

from atools_python.common import dereplicate


def test_dereplicate():
    """测试有序删除重复元素 的方法：dereplicate"""
    # 测试普通类型
    list1 = [1, 7, 8, 2, 4, 1, 5, 4, 8, 1, 7, 9, 4, 3]
    print(list1)
    assert dereplicate(list1) == [1, 7, 8, 2, 4, 5, 9, 3]

    # 测试dict类型
    a = [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
    list1 = list(dereplicate(a, key=lambda d: (d['x'], d['y'])))
    assert list1 == [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
    list1 = list(dereplicate(a, key=lambda d: d['x']))
    assert list1 == [{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]


if __name__ == '__main__':
    pytest.main()

# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018/10/13
"""
import os
import re
import numpy as np
import pandas as pd


def process_content(data):
    """对content列进行处理
    """
    pass
    return data


if __name__ == "__main__":
    # 初始化DataFrame
    # data_pd = pd.read_excel(os.path.join(""))
    # data_pd = data_pd.sample(frac=0.1)
    print('初始化DataFrame完毕')

    # 开始处理DataFrame
    # 1. 构造完整的DataFrame

    # 2. 针对某些项逐个处理
    # data_pd['content'] = data_pd['content'].map(lambda x: process_content(x))
    print('处理DataFrame完毕')

    # 处理完毕，保存DataFrame
    # data_pd.to_csv()
    print('保存DataFrame完毕')
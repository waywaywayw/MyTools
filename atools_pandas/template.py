# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018/10/13
"""
import os
import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from atools_pandas.my_pandas import drop_rows


def process_content(data):
    """对content列进行处理
    """
    pass
    return data


if __name__ == "__main__":
    # 初始化DataFrame
    # input_path = os.path.join("")
    # data_pd = pd.read_excel(input_path)
    # data_pd = data_pd.sample(frac=0.1)
    print('初始化DataFrame完毕')

    # 开始处理DataFrame
    # 1. 构造完整的DataFrame
    # 2. 针对某些项逐个处理
    # data_pd['content'] = data_pd['content'].map(lambda x: process_content(x))
    print('处理DataFrame完毕')

    # 处理完毕，保存DataFrame
    # train_data_pd, test_data_pd = train_test_split(data_pd, test_size=0.1, random_state=2018)
    # train_data_pd.to_csv()
    print('保存DataFrame完毕')
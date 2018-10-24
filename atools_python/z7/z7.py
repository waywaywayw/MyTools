# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018/10/22
"""
import os
import re
import subprocess
import time

from atools_python.files import readlines_from_file, file_no_suffix

# 7z压缩软件的下载地址：https://www.7-zip.org/download.html
# z7_path = os.path.join('atools_python', 'z7', '7z.exe')
z7_path = os.path.join('7z.exe')


def z7_extract_cmd(compressed_file_path, output_path, pwd=None, error_output=False):
    """
    生成解压命令。（命令行版的7z）
    :param compressed_file_path: 待解压文件的路径
    :param output_path: 解压文件输出路径（一般是输出到当前文件夹）
    :param pwd: 密码（可选）
    :param error_output: 是否显示执行命令行时错误信息（默认不显示）
    :return: 解压命令
    """
    # bse0 表示不显示错误输出；aoa 表示覆盖已有文件；y表示所有选项都点同意
    cmd = '{} x "{}" -y -o"{}" -aoa '.format(z7_path, compressed_file_path, output_path)

    if not error_output:  # 错误信息
        cmd += '-bse0 '
    if pwd:  # 密码
        cmd += '-p{} '.format(pwd)
    return cmd


def z7_extract(compressed_file_path, output_path, pwd=None, error_output=False, verbose=True):
    """
    使用命令行，执行z7的解压命令
    :param compressed_file: 待解压文件的路径
    :param output_path: 解压文件输出路径（一般是输出到当前文件夹）
    :param pwd: 密码（可选）
    :param error_output: 是否显示执行命令行时错误信息（默认不显示）
    :param verbose: 是否输出调试信息（默认显示）
    :return: 解压成功返回True；失败返回False
    """
    cmd = z7_extract_cmd(compressed_file_path, output_path, pwd=pwd, error_output=error_output)
    if verbose:
        print('待执行的解压命令：', cmd)

    # 开始执行解压命令
    start_time = time.time()
    # 第一种执行命令的方式（直接执行C接口的命令行，只返回命令返回值）
    # res = os.system(cmd)
    # 第二种执行命令的方式（subprocess模块。推荐，可选参数较多）
    # 调用示例1：https://www.cnblogs.com/breezey/p/6673901.html
    # 调用示例2（推荐）：https://www.cnblogs.com/yyds/p/7288916.html
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    # print(ret)
    # 输出stdout的示例：print(ret.stdout.decode('gbk'))
    if verbose:
        print('解压命令耗时：{} 秒'.format(time.time()-start_time))
    if ret.returncode == 0:
        return True
    else:
        return False


def z7_try_pwd_list(compressed_file_path, output_path, pwd_list=(), verbose=False):
    """
    尝试密码列表。
    :return: 成功找到密码，返回成功的密码项；失败返回None
    """
    # 挨个尝试密码
    for pwd in pwd_list:
        if verbose:
            print('开始尝试密码: ', pwd)
        # 因为尝试密码过程中有很多错误，所以指定不显示错误信息
        ret = z7_extract(compressed_file_path, output_path, pwd=pwd, error_output=False, verbose=verbose)
        if ret:
            if verbose:
                print('解压成功, 密码为: ', pwd)
            return pwd
    return None


if __name__ == '__main__':
    input_path = os.path.join('D:\\', 'BaiduNetdiskDownload', '预览图带名字.zip')
    passwd_path = os.path.join('passwd.txt')

    pwds = readlines_from_file(passwd_path)
    ret = z7_try_pwd_list(input_path, file_no_suffix(input_path), pwds)
    print('解压命令执行情况:', ret)

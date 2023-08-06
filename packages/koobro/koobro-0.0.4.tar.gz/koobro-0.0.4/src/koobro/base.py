import os


def output(value, newline=False):
    """
    输出变量

    :param value: 变量
    :param newline: 是否换行
    :return:
    """
    if newline:
        print(f'表达式：{repr(value)} \n 类型：{type(value)} \n 值：{value}')
    print(f'表达式：{repr(value)} ----- 类型：{type(value)} ----- 值：{value}')


def create_dir(dir_path):
    """
    如果目录不存在，则创建目录

    :param dir_path: 目录路径
    :return:
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

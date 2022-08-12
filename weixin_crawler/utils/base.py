# 日志打印
from loguru import logger

# 对齐打印且能通过depth控制打印深度
import pprint
pp = pprint.PrettyPrinter(depth=6)
debug_p = pp.pprint


def validate_file_name(file_name):
    """
    :param file_name:等待验证的文件名
    :return: 验证windows文件名的合法性 将不合法的字符替换为 下划线_
    """
    import re
    rstr = r"[\/\\\:\*\?\"\<\>\|\“\”]"  # '/ \ : * ? " < > |'
    new_file_name = re.sub(rstr, "_", file_name)  # 替换为下划线
    return new_file_name


def the_platform():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return 'linux'
    elif platform == "darwin":
        return 'osx'
    elif platform == "win32":
        return 'win'

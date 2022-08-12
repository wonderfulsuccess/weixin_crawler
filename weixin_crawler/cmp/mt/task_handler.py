import time
from random import random


def task_handler(task=None):
    """
    :return: 模拟执行一个任务
    """
    # 随眠0到5秒
    sleep_time = round(random()*5, 1)
    time.sleep(sleep_time)
    print('执行任务', task, '用时', sleep_time)


if __name__ == '__main__':
    task_handler()

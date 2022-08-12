"""
生成阶主程序的入口
"""

from threading import Thread
from multiprocessing import Process
import multiprocessing
from web_server import run_webserver
from cmp.proxy_server import start_proxy
import webbrowser
import time


def proxy_server():
    """
    :return:运行代理服务
    """
    start_proxy()


def other_tasks():
    """
    :return: 其余需要周期性运行的任务
    """
    from app.api.crawler import ReqData
    while True:
        ReqData().send()
        time.sleep(3)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    Process(target=proxy_server).start()
    Thread(target=other_tasks).start()
    webbrowser.open('http://localhost:5000')
    run_webserver()

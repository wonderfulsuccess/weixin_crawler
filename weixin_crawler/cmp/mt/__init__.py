"""
多线程模块 准备好处理每个任务的方法 任务队列 设置需要的线程数量即可
先将任务放入任务队列中 让后用n个线程去处理这些任务直到任务完成 run_mt 先修改prepare_tasks和task_handler 最终调用的对象
"""
import threading
from queue import Queue
import queue
from utils.base import logger
from cmp.mt.task_handler import task_handler as default_task_handler
from cmp.mt.prepare_tasks import prepare_tasks as default_prepare_tasks

task_handler = default_task_handler
prepare_tasks = default_prepare_tasks


class Worker(threading.Thread):
    """
    继承threading.Thread 定义任务处理类
    1. 从任务队列中取出一个任务
    2. 从代理IP队列中取出一个IP 发起请求 如果请求成功将代理IP放回队列 否者重新申请一个代理IP再次发起请求直到成功
    """
    def __init__(self,task_q):
        """
        :param task_q: 任务队列
        """
        threading.Thread.__init__(self)
        self.task_q = task_q
        self.thread_stop=False

    def run(self):
        """
        :return: 直到线程结束
        """
        while not self.thread_stop:
            result = self.do_job()
            if result is None:
                self.thread_stop=True
                break

    def stop(self):
        self.thread_stop = True

    @property
    def get_q_task(self):
        """
        :return: 尝试从任务队列中取出一个任务
        """
        try:
            task = self.task_q.get(block=True, timeout=20)
            return task
        except queue.Empty:
            return None

    def do_job(self):
        """
        :return: 取出一个任务 请求html内容
        """
        task = self.get_q_task
        if task is None:
            return
        try:
            # 执行任务
            # logger.info('正在执行任务 '+str(task))
            task_handler(task)
        except Exception as e:
            logger.error("任务出错"+(str(task)))
            logger.error(e)
        self.task_q.task_done()
        return task


class WorkerService():
    """
    服务于Worker，代理IP的数量和线程的数量可以不一致
    """
    def __init__(self, task_q):
        self.task_q = task_q
        # 线程数量
        self.worker_num = None
        # 任务
        self.tasks = prepare_tasks()
        # 任务总数
        self.task_num = 0

    def create_task_q(self,num=None):
        """
        :return: 创建任务队列 将待爬取的文章加入任务队列 返回任务总数
        """
        c = 0
        for task in self.tasks:
            self.task_q.put(task, block=True, timeout=None)
        self.task_num = c
        return c


class DOJOB():
    """
    多线程开始工作
    """
    def __init__(self):
        self.task_q = Queue()
        # workerservice实例
        self.ws = None
        self.workers = []

    def prepare_tasks(self, worker_num):
        self.ws = WorkerService(self.task_q)
        task_num = self.ws.create_task_q()
        self.workers = []
        for i in range(worker_num):
            self.workers.append(Worker(self.task_q))
        return task_num

    def run_wrokers(self):
        for worker in self.workers:
            worker.start()

    def join_workers(self):
        for worker in self.workers:
            worker.join()


def run_mt(tn=20, _prepare_tasks=None, _task_handler=None):
    """
    :param tm: 线程数量
    :return: 开始多线程工作
    """
    # 如果有传入准别任务和处理任务的函数则取代
    global prepare_tasks, task_handler
    if _prepare_tasks:
        prepare_tasks = _prepare_tasks
    if _task_handler:
        task_handler = _task_handler
    djb = DOJOB()
    djb.prepare_tasks(tn)
    djb.run_wrokers()
    djb.join_workers()

if __name__ == "__main__":
    run_mt(100)


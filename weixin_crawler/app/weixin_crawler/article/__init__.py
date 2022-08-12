"""
得到的请求参数全部的微信账号进行采集
多线程爬取微信公众号文章正文
使用前提条件：
1. 数据库有文章的永久链接
2. 代理IP地址有效
"""
import threading
import os
import codecs
from lxml.etree import tostring
from queue import Queue
import requests
from requests.exceptions import SSLError, Timeout, ProxyError, ConnectionError
import queue
import time
from cmp.proxy import get_proxy_ip
from copy import copy
from cmp.db.mongo import CollectionOperation
from utils.base import logger
from utils.data_process import get_md5
from instance import user_settings
# 是否需要保存html文档 初始数据库没有该字段 需要先判断
if 'save_html' in user_settings.get():
    save_html = user_settings.get()['save_html']
else:
    save_html = 'false'
# 混存采集的文章数据 最后一次性插入数据库可以提高采集速度 暂时未采用该方案
article_data_buffer = []
# 当亲采集公众号的昵称
nickname = None
# 采集进度实例 发送给其前端
front_process = None
# 数据库操作
col_data = None


class Worker(threading.Thread):
    """
    继承threading.Thread 定义任务处理类
    1. 从任务队列中取出一个任务
    2. 从代理IP队列中取出一个IP 发起请求 如果请求成功将代理IP放回队列 否者重新申请一个代理IP再次发起请求直到成功
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    def __init__(self,task_q, ip_q):
        """
        :param task_q: 任务队列
        :param ip_q: 代理IP队列
        """
        threading.Thread.__init__(self)
        self.task_q = task_q
        self.ip_q = ip_q
        self.thread_stop=False

    def run(self):
        """
        :return: 直到线程结束
        """
        while not self.thread_stop:
            result = self.get_html()
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

    def new_proxy_ip(self):
        """
        :return: 申请一个代理IP
        """
        # input("获取新代理 回车确认")
        proxy_ip = get_proxy_ip()
        # 没有配置付费代理IP服务 无法采集 清空任务队列
        if not proxy_ip:
            self.task_q.clear()
            logger.error('采集文章正文:'+'IP地址被限制！采集文章正文已经提前结束，将导致部分文章的PDF无法导出，可24小时后再次采集，亦可联系阿呆。将继续采集阅读数据')
        # print("新代理ip为",proxy_ip)
        TaskRecoder.add_ip_log(ip=proxy_ip, created_time=time.time())
        return proxy_ip

    def get_proxy_ips(self,all=False):
        """
        :param all: True全部取出 False取出下一个可用的代理
        :return: 取出代理IP
        """
        if self.ip_q.qsize():
            ips = self.ip_q.get(block=True, timeout=None)
            self.ip_q.put(ips, block=True, timeout=None)
            if all:
                return ips['ips']
            else:
                return ips['ips'][ips['next_ip']],ips['next_ip']
        else:
            exit("代理IP队列出现错误")

    def update_proxy_ip(self, proxy_ip, index):
        """
        :param proxy_ip:
        :return: 更新队列中的proxy_ip 返回队列中代理IP的数量
        """
        ips = self.ip_q.get(block=True, timeout=None)
        ips['ips'][index] = proxy_ip
        self.ip_q.put(ips, block=True, timeout=None)
        return len(ips['ips'])

    def shift_next_proxy_ip(self):
        """
        :return:next_ip有效自增
        """
        ips = self.ip_q.get(block=True, timeout=None)
        ips['next_ip'] = (ips['next_ip']+1) % (len(ips['ips']))
        self.ip_q.put(ips, block=True, timeout=None)
        return ips['next_ip']

    def get_html(self):
        """
        :return: 取出一个任务 请求html内容
        """
        task = self.get_q_task
        if task is None:
            return None
        proxy_ip,index = self.get_proxy_ips()
        requests_done = False
        r_text = None
        proxy_failed = False
        content_url = copy(task['content_url'])
        while not requests_done:
            try:
                if '127.0.0.1' in proxy_ip['ip']:
                    if 'https' not in task['content_url']:
                        task['content_url'] = task['content_url'].replace('http','https')
                    r = requests.get(url = task['content_url'],
                                     headers = self.headers,
                                     timeout = 5)
                else:
                    r = requests.get(url = task['content_url'],
                                     headers = self.headers,
                                     timeout = 5,
                                     proxies = {"http":proxy_ip['ip'],"https":proxy_ip['ip']})
                r_text = r.text
                # 判断IP被限制
                if ("访问过于频繁，请用微信扫描二维码进行访问" in r_text) or ("<title>验证</title>" in r_text) or ("IP Address:" in r_text):
                    logger.error('IP被限制:'+task['content_url'])
                    TaskRecoder.add_failed_info(proxy_ip['ip'],"IP被限制")
                    if TaskRecoder.should_ask_new_ip(proxy_ip['ip']):
                        proxy_ip['ip'] = self.new_proxy_ip()
                    proxy_failed = True
                # 获得了正常的数据存入数据库
                else:
                    # global article_data_buffer
                    article_data = DecodeArticle.decode_content(r_text, need_content=True)
                    article_data['id'] = get_md5(task['content_url'].replace('https', 'http'))
                    # 是否需要保存html
                    if save_html == 'true':
                        DecodeArticle.save_html_as_file(nickname=nickname, file_name=article_data['id'], html_str=r_text)
                    # 当前采集的文章插入数据库
                    col_data.insert('id', article_data)
                    # SQLite中 为加快速度 先缓存数据 最后批量插入数据库 mongodb无此性能限制
                    # article_data_buffer.append(article_data)
                    # save_article()
                    requests_done = True

            # requests异常总结 https://blog.csdn.net/weixin_39198406/article/details/81482082
            except ProxyError:
                proxy_failed = True
                print(task['id'], proxy_ip, "ProxyError",task['content_url'])
                TaskRecoder.add_failed_info(proxy_ip['ip'],"ProxyError")
                if TaskRecoder.should_ask_new_ip(proxy_ip['ip']):
                    proxy_ip['ip'] = self.new_proxy_ip()
            except SSLError:
                proxy_failed = True
                print(task['id'], proxy_ip, "SSLError")
                TaskRecoder.add_failed_info(proxy_ip['ip'],"SSLError")
                if TaskRecoder.should_ask_new_ip(proxy_ip['ip']):
                    proxy_ip['ip'] = self.new_proxy_ip()
            except Timeout:
                proxy_failed = True
                print(task['id'], proxy_ip, "Timeout")
                TaskRecoder.add_failed_info(proxy_ip['ip'],"Timeout")
                if TaskRecoder.should_ask_new_ip(proxy_ip['ip']):
                    proxy_ip['ip'] = self.new_proxy_ip()
            except ConnectionError:
                proxy_failed = True
                print(task['id'], proxy_ip, "ConnectionError")
                TaskRecoder.add_failed_info(proxy_ip['ip'],"ConnectionError")
                if TaskRecoder.should_ask_new_ip(proxy_ip['ip']):
                    proxy_ip['ip'] = self.new_proxy_ip()
            except Exception as e:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(e).__name__, e.args)
                print(message)

        self.task_q.task_done()
        # 如果IP更新过
        if proxy_failed:
            self.update_proxy_ip(proxy_ip, index)
        # 准备好下次代理需要使用的IP
        self.shift_next_proxy_ip()
        # 更新任务日志
        TaskRecoder.update_ip_log(proxy_ip['ip'])
        # 打印任务状态
        TaskRecoder.print_ts_brief()
        # 此处增加存入数据库代码
        return r_text

    def response_check(self, r):
        """
        :param r:
        :return: 判断请求相应是否是有效的文章html
        """
        pass


class WorkerService():
    """
    服务于Worker，代理IP的数量和线程的数量可以不一致
    """
    def __init__(self, nickname, task_q, ip_q):
        """
        :param nickname: 需要爬取公众号文章的昵称
        :param task_q: 全局可见任务队列
        :param ip_q: 全局可见代理IP队列
        """
        self.task_q = task_q
        self.ip_q = ip_q
        self.nickname = nickname
        # 需要爬取文章清单的生成器 article 字段为空的文章 html太大已经不再存放进入数据库 而是作为静态文件放在web_server下
        self.articles_gen = col_data.get(article={"$exists": False})
        # 文章总数
        self.articles_num = col_data.count(article={"$exists": False})
        # 任务总数
        self.task_num = 0
        logger.debug("%s共有%d篇文章"%(self.nickname, self.articles_num))
        # 任务开始时间
        self.begin_time = time.time()
        # 是否只使用一个代理IP
        self.is_one_proxy = None
        # 线程数量
        self.worker_num = None

    def create_task_q(self):
        """
        :return: 创建任务队列 将待爬取的文章加入任务队列
        """
        index = 0
        for a in self.articles_gen:
            # 有些文章的连接并不是来自微信服务器 排除掉 只采集没有comment_id的文章 因为有comment_id的肯定已经采集过
            if "mp.weixin.qq.com" in a['content_url']:
                index += 1
                task = {'nickname': a['nickname'], 'title': a['title'], 'content_url': a['content_url'], 'id': index}
                self.task_q.put(task, block=True, timeout=None)
        self.task_num = index
        logger.debug("%s共有%d篇文章需要爬取"%(self.nickname, self.task_num))
        # 记录总任务数
        TaskRecoder.set_total_task_num(self.task_num)
        return self.task_num

    def init_proxy_ips(self, ip_num=1, proxy=False):
        """
        :param ip_num: 代理的数量
        :param proxy: 是否需要使用代理否者代理IP全部为 127.0.0.1:80 如果proxy为False代理ip默认为一个127.0.0.1:80
        :return: 初始化代理IP队列
        队列只有一个任务 数据类型为dict
        {'ips':[{'ip':ip,'delay':0,'alive_time':0,'cunter':0},{***},{***}],
         'next_ip':0}
        ips是全部可用ip的list
        next_ip有上一次使用的进程更新 下一个进程使用其确定使用哪个ip
        """
        ips = []
        self.is_one_proxy = True
        # 不使用代理
        if proxy==False:
            ips = '127.0.0.1:80'
        # 使用代理
        else:
            if ip_num == 1:
                ips = get_proxy_ip()
            else:
                ips = [get_proxy_ip() for i in range(ip_num)]
                self.is_one_proxy = False
        if type(ips) == str:
            ips = [ips]
        ip_queue_data = {}
        ip_queue_data['ips'] = []
        ip_queue_data['next_ip'] = 0
        for ip in ips:
            logger.debug(ip)
            # ip,延迟,已经使用的时长,使用的次数
            ip_queue_data['ips'].append({'ip':ip,'delay':0,'alive_time':0,'cunter':0})
            # 新申请的代理ip加入ts
            TaskRecoder.add_ip_log(ip=ip,created_time=time.time())
        self.ip_q.put(ip_queue_data, block=True, timeout=None)
        logger.debug(ip_queue_data)
        logger.debug("代理IP队列已经初始化完毕 共有%d个代理代理IP"%(self.ip_q.qsize()))


class TaskRecoder():
    """
    记录任务执行过程中的信息
    """
    task_log_data = {
        'ips_index':[],     # 代理ip索引['ip1','ip2']
        'ips':{},           # 代理ip日志 单元为ip_log
        'total_task_num':0, # 总任务
        'done_task_num':0,  # 实际完成的任务
        'ip_used':0,        # 使用过的ip数量
        'begin_time':0,     # 任务开始时间
        'speed':0,          # 总体速度
        'worker_num':0,     # 线程数
    }
    ip_log = {
        'ip':'',            # 代理ip地址
        'created_time':0,   # 代理ip申请时间
        'last_time':0,      # 最后一次使用时间
        'used_unm':0,       # 使用次数
        'speed':0,          # 平均速度 完成一次请求需要的秒
        'failed':0,         # 失败次数
        'reason':[],        # 失败原因
    }
    task_status_q = None
    @staticmethod
    def init_queue(task_status_q):
        TaskRecoder.task_status_q = task_status_q
        ts = copy(TaskRecoder.task_log_data)
        ts['begin_time'] = time.time()
        TaskRecoder.task_status_q.put(ts, block=True, timeout=None)

    @staticmethod
    def set_total_task_num(total_task_num):
        ts = TaskRecoder.get_ts()
        ts['total_task_num'] = total_task_num
        result = TaskRecoder.put_ts(ts)
        if result == None:
            logger.error("任务状态队列出错")
            exit()

    @staticmethod
    def set_worker_num(worker_num):
        ts = TaskRecoder.get_ts()
        ts['worker_num'] = worker_num
        TaskRecoder.put_ts(ts)

    @staticmethod
    def add_ip_log(**kwargs):
        """
        :param kwargs:
        :return: 根据'ip'更新代理ip的日志 ip参数必须指定
        """
        # ip用过
        ip = kwargs['ip']
        ts = TaskRecoder.get_ts()
        if ip in ts['ips_index']:
            ts['ips'][ip].update(kwargs)
        # ip没用过
        else:
            ts['ips_index'].append(ip)
            ip_log = copy(TaskRecoder.ip_log)
            ip_log.update(kwargs)
            ts['ips'][ip] = ip_log
            ts['ip_used'] += 1
        TaskRecoder.put_ts(ts)

    @staticmethod
    def counter_plus(ip):
        ts = TaskRecoder.get_ts()
        ts['ips'][ip]['used_unm'] += 1
        TaskRecoder.put_ts(ts)

    @staticmethod
    def update_ip_log(ip):
        """
        :param ip:
        :return: 当代理ip完成一次爬取之后调用该方法自动计算机相关数据
        """
        ts = TaskRecoder.get_ts()
        ts['ips'][ip]['used_unm'] += 1
        ts['ips'][ip]['last_time'] = time.time()
        ts['ips'][ip]['speed'] = round((ts['ips'][ip]['last_time']-ts['ips'][ip]['created_time'])/ts['ips'][ip]['used_unm'],3)
        ts['done_task_num'] += 1
        ts['speed'] = round((time.time()-ts['begin_time'])/ts['done_task_num'], 3)
        TaskRecoder.put_ts(ts)

    @staticmethod
    def add_failed_info(ip,failed_reason):
        """
        :param ip:
        :param failed_reason:
        :return: 添加ip失败标记
        """
        ts = TaskRecoder.get_ts()
        ts['ips'][ip]['failed'] += 1
        ts['ips'][ip]['reason'].append(failed_reason)
        TaskRecoder.put_ts(ts)

    @staticmethod
    def get_failed_num(ip):
        ts = TaskRecoder.get_ts()
        TaskRecoder.put_ts(ts)
        return ts['ips'][ip]['failed']


    @staticmethod
    def should_ask_new_ip(ip):
        """
        :return: 对于一个刚才发生失败请求的IP是否应该申请新IP
        如果一IP失败的次数小于 线程数 则不应该申请新IP
        """
        ts = TaskRecoder.get_ts()
        TaskRecoder.put_ts(ts)
        failed_num = ts['ips'][ip]['failed']
        worker_num = ts['worker_num']
        logger.warning("ip:%s 失败次数:%d 任务总数:%d"%(ip,failed_num,worker_num))
        if failed_num < worker_num:
            return False
        else:
            # 防止其余线程继续申请ip
            ts = TaskRecoder.get_ts()
            ts['ips'][ip]['failed'] = 0
            TaskRecoder.put_ts(ts)
            return True


    @staticmethod
    def get_ts():
        """
        :return: 从队列中获取任务状态
        """
        if TaskRecoder.task_status_q.qsize()==0:
            return None
        ts = TaskRecoder.task_status_q.get(block=True, timeout=None)
        return ts

    @staticmethod
    def put_ts(ts):
        """
        :param ts: 将任务状态存瑞任务队列中
        :return:
        """
        if TaskRecoder.task_status_q.qsize()==1:
            return None
        TaskRecoder.task_status_q.put(ts, block=True, timeout=None)
        return ts

    @staticmethod
    def print_ts():
        ts = TaskRecoder.get_ts()
        TaskRecoder.put_ts(ts)
        logger.info(ts)

    @staticmethod
    def print_ts_brief():
        ts = TaskRecoder.get_ts()
        TaskRecoder.put_ts(ts)
        # 准备任务日志信息
        item = {}
        item['style'] = '采集正文'
        item['nickname'] = '略'
        item['process'] = '%d/%d'%(ts['done_task_num'], ts['total_task_num'])
        item['data'] = '速度%.3f'%(ts['speed'])
        item['task'] = '略'
        # send_crawling_log_info(item)
        logger.info("速度%.3f 完成%d/%d"%(ts['speed'],ts['done_task_num'], ts['total_task_num']))
        # 报告状态给前端
        if front_process:
            front_process.new_article(ts['done_task_num'], ts['total_task_num'], ts['ips'], ts['speed'])
        # send_status_info('采集文章正文中...','完成率%d/%d'%(ts['done_task_num'], ts['total_task_num']))

    @staticmethod
    @property
    def ip_used():
        ts = TaskRecoder.get_ts()
        TaskRecoder.put_ts(ts)
        return ts['ip_used']


class RequestContent():
    """
    多线程爬取微信公众号的文章正文
    """
    def __init__(self):
        self.task_q = Queue()
        self.ip_q = Queue()
        TaskRecoder.init_queue(Queue())
        # workerservice实例
        self.ws = None
        self.workers = []

    def prepare_articles(self, nickname, worker_num=16, ip_num=1, need_proxy=False):
        """
        :param nickname: 公众号昵称用于从数据库中获取需要爬取内容的文章
        :param worker_num: 通过发起请求的线程数量
        :param ip_num: 使用的代理IP数量
        :param need_proxy: 是否需要设置代理，设置为不需要，如果被限制会自动使用代理
        :param one_proxy: 是否使用同一个代理IP进行多线程请求
        :return:
        """
        self.ws = WorkerService(nickname,self.task_q,self.ip_q)
        task_num = self.ws.create_task_q()
        self.ws.init_proxy_ips(ip_num=ip_num, proxy=need_proxy)
        TaskRecoder.set_worker_num(worker_num)
        TaskRecoder.print_ts()
        self.workers = []
        for i in range(worker_num):
            self.workers.append(Worker(self.task_q,self.ip_q))
        return task_num

    def run_crawlers(self):
        for worker in self.workers:
            worker.start()

    def join_cralwers(self):
        for worker in self.workers:
            worker.join()


REG_NICKNAME = r'nickname">\n\S*?</strong>'
REG_VIDEO_NUM = r'video_iframe'
REG_PIC_NUM = r'<img '
REG_COMMENT_ID = r'comment_id = "\S*?"'
import re
import html2text
html_to_text = html2text.HTML2Text()

class DecodeArticle():
    """
    解析文章内容
    """
    @staticmethod
    def decode_content(r, need_content = True):
        """
        :param r:html字符串
        :return:解析文章html
        文章html中包含的信息非常丰富 不仅仅只有文章文本等基本数据还有comment_id
        video_num pic_num 还有原文的markdown信息
        """
        data = {}
        r_data = r
        data['video_num'] = len(re.findall(REG_VIDEO_NUM, r_data))
        data['pic_num'] = len(re.findall(REG_PIC_NUM, r_data))
        data['comment_id'] = re.findall(REG_COMMENT_ID, r_data)
        if len(data['comment_id'])==1:data['comment_id']=data['comment_id'][0].split('"')[1]
        else:data['comment_id'] = str(0)
        if need_content:
            # 不将html存入数据库 而是存入 磁盘文件中
            # data['html'] = r
            try:
                r_data = DecodeArticle.part_of_html(r_data)
                # 提取文档中的html中的文本 并且去掉换行
                data['article'] = html_to_text.handle(r_data).replace('\n','')
            except Exception as e:
                try:
                    data['article'] = html_to_text.handle(r).replace('\n','')
                except:
                    data['article'] = ""
        return data

    @staticmethod
    def save_html_as_file(nickname, file_name, html_str):
        """
        :param nickname: 公众号的昵称用作文件夹
        :param html_str: html内容
        :param file_name: 文件名
        :return: 将文章的html内容保存为文件 存储在web_server的static/html/nickname路径下
        """
        path = './web_server/static/html/'+nickname+'/'
        if not os.path.exists(path):
            os.makedirs(path)
        whole_name = path+file_name+'.html'
        # 文件不存在才保存html
        if not os.path.isfile(whole_name):
            file = codecs.open(whole_name, "w", "utf-8")
            file.write(html_str.replace('data-src','src'))
            file.close()
        else:
            logger.debug('HTML已存在 %s'%(whole_name))

    @staticmethod
    def part_of_html(raw_html,x_path=r'//div[@id="js_content"]'):
        """
        :param x_path:xpath表达式默认获取微信公众号的正文xpath
        :param raw_html:r.text
        :return: 截取html的一部分
        """
        from lxml import html
        tree = html.fromstring(raw_html)
        data = tree.xpath(x_path)
        if len(data) == 1:
            data = tostring(data[0], encoding='unicode')
            return data
        else:
            return raw_html


def save_article(windos=200):
    """
    :return: article_data_buffer当到达一定长度之后 保存并清空
    """
    global article_data_buffer
    success = False
    if len(article_data_buffer) >= windos:
        # 数据库有可能在忙无法保存成功
        while not success:
            try:
                col_data.insert(id, article_data_buffer)
                article_data_buffer = []
                logger.info('保存成功保存%d'%(windos))
                success = True
            except:
                time.sleep(3)
                save_article(windos=windos)


def use_proxy_directly():
    """
    :return: 是否直接使用代理
    """
    from instance import user_settings
    settings = user_settings.get()
    if 'use_proxy' in settings:
        # 用户决定优先使用真实IP 不直接使用代理 需要再说
        if settings['use_proxy'] == 'true':
            return False
        else:
            return True
    else:
        return False


def get_all_article(worker_num=128, process=None):
    global article_data_buffer, nickname, front_process, col_data
    front_process = process
    article_data_buffer = []
    from instance import rd
    nickname = rd.tidy()[0]['nickname']
    # 重新赋值数据库操作实例
    col_data = CollectionOperation(nickname)
    rc = RequestContent()
    # 采集文章内容进入新阶段
    task_num = rc.prepare_articles(nickname, worker_num=worker_num, ip_num=1, need_proxy=use_proxy_directly())
    # 没有任务直接返回
    if not task_num:
        return
    rc.run_crawlers()
    rc.join_cralwers()
    # 保存最后尾巴
    # save_article(windos=1)
    TaskRecoder.print_ts()

def get_all_article_by_nickname(_nickname, worker_num=128, process=None):
    global article_data_buffer, nickname, front_process, col_data
    front_process = process
    article_data_buffer = []
    nickname = _nickname
    # 重新赋值数据库操作实例
    col_data = CollectionOperation(nickname)
    rc = RequestContent()
    task_num = rc.prepare_articles(nickname, worker_num=worker_num, ip_num=1, need_proxy=use_proxy_directly())
    # 没有任务直接返回
    if not task_num:
        return
    # 采集文章内容进入新阶段
    rc.run_crawlers()
    rc.join_cralwers()
    # 保存最后尾巴
    # save_article(windos=1)
    TaskRecoder.print_ts()

if __name__ == "__main__":
    get_all_article_by_nickname('人民日报')


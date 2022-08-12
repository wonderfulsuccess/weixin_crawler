"""
调度和管理爬虫采集一个公众号中所有没有阅读数据的文章
"""
from instance import rd
from utils.base import logger,debug_p
from utils.data_process import get_md5
from cmp.db.mongo import CollectionOperation
import time
from instance import stop_and_start
from app.weixin_crawler.reading_data.crawler import Crawler


class ReadingData():
    def __init__(self):
        # 从数据源获取的请求参数
        self.wx_req_data_list = rd.tidy()
        # 微信昵称
        self.nickname = self.wx_req_data_list[0]['nickname']
        # 同一个微信账号两次请求之间的时间间隔
        self.every_delay = 3.0
        # 参加采集微信的数量
        self.wx_num = len(self.wx_req_data_list)
        # 多个微信账号的情况下时间间隔
        self.delay = round(self.every_delay/self.wx_num, 3)
        # 所有需要采集的文章
        self.articles = []
        # 数据库操作
        self.col_data = CollectionOperation(self.nickname)
        # 上一次请求时间
        self.pre_crawl_time = time.time()

    def get_all_reading_data(self, process=None, mov=10):
        """
        :param mov: 10~17
        :return: 轮流调用wx_req_data_list中的微信参数 采集文章的阅读数据
        """
        # 获取所有需要采集的文章url
        # 将url等参数传递给新建的爬虫对象
        # 保存数据
        if 'getappmsgext' in self.wx_req_data_list[0]:
            # 从书库库获取需要采集的文章列表
            # raw_articles = self.col_data.get(read_num={"$exists": False})
            # 选中没有阅读数据且位置低于mov的文章来采集阅读数据
            raw_articles = self.col_data.table.find({"$and":[ {"read_num":{"$exists": False}}, {"mov":{"$lte": int(mov)}}]})
            # 采集阅读数据需要较长时间 防止长时间占用数据库游标 缓存需要采集的文章列表
            cnt = 0
            for a in raw_articles:
                # [cnt, url, comment_id]
                if "mp.weixin.qq.com" in a['content_url']:
                    # 在采集文章正文之前采集阅读数据 这时 并没有comment_id
                    if 'comment_id' not in a:
                        a['comment_id'] = 0
                    self.articles.append([cnt, a['content_url'], a['comment_id']])
                    cnt += 1
            # 一个一个开始采集
            for itme in self.articles:
                while time.time()-self.pre_crawl_time <= self.delay:
                    time.sleep(0.05)
                self.pre_crawl_time = time.time()
                reading_data = Crawler(itme[1], itme[2], self.wx_req_data_list[itme[0]%self.wx_num]).run()
                # 开始安检 使用安检之后的数据 因为它一定是合格的数据
                reading_data = self.check(reading_data, itme)
                # 安检通过
                reading_data['id'] = get_md5(itme[1])
                self.col_data.insert('id', reading_data)
                # 发送进度数据给前端
                process.new_reading_data(itme[0]+1, len(self.articles), self.delay)
            # 使用多线程 同时采集所有的文章 测试证明不可行 容易被限制
            # from cmp.mt import run_mt
            # run_mt(len(self.articles), self.prepare_task, self.task_handler)
        else:
            logger.warning('点击查看该公众号的任意一篇文章且出现阅读量')

    def save(self, reading_data):
        """
        :param reading_data:
        :return: 保存数据
        """
        pass

    def prepare_task(self):
        """
        :return: 多线程的方式准备任务
        """
        for item in self.articles:
            yield {'index':item[0], 'url':item[1]}

    def task_handler(self, task):
        """
        :return: 多线程的方式任务处理器
        """
        Crawler(task['url'], self.wx_req_data_list[task['index']%self.wx_num]).run()

    def check(self, reading_data, item):
        """
        :return: 带着本次请求的参数和结果一起过安检
        请求失败导致安检不通过 安检提醒人重新操作手机 操作完之后再次发起请求
        不排除还是会失败  继续调用自己 反正想办法让其获得成功的请求  最后返回成功的请求
        """
        if reading_data != 'req_data_error':
            stop_and_start.check({'crawler': '阅读数据', 'msg': 'success'})
        else:
            # 先过安检 安检会提醒更新参数
            stop_and_start.check({'crawler': '阅读数据', 'msg': 'req_data_error'})
            # 参数更新完毕 从数据源读取参数 继续请求
            self.wx_req_data_list = rd.tidy()
            # 参数有可能被用户删除了 循环检查
            while len(self.wx_req_data_list) == 0:
                self.wx_req_data_list = rd.tidy()
                from utils.front import notification
                notification('没有发现参数','参数错误',_type='error')
                time.sleep(3)
            reading_data = Crawler(item[1], item[2], self.wx_req_data_list[0]).run()
            # 继续安检
            self.check(reading_data, item)
        return reading_data

"""
为采集页面提供数据和操作支持 整理符合前端显示格式的数据
"""
from instance import rd
from utils.base import debug_p
from web_server import socketio
from datetime import datetime
import time


class ReqData():
    """
    为前端准备请求参数的显示
    """
    def __init__(self):
        self.wx_req_data_list = rd.tidy()


    def get(self):
        """
        :return: 所有的数据
        """
        data = []
        for wxrd in self.wx_req_data_list:
            item = {}
            item['more'] = '0'
            if 'load_more' in wxrd:
                item['more'] = wxrd['load_more']['time']

            item['reading'] = '0'
            if 'getappmsgext' in wxrd:
                item['reading'] = wxrd['getappmsgext']['time']

            item['nickname'] = '?'
            if 'nickname' in wxrd:
                item['nickname'] = wxrd['nickname']

            item['nick_name'] = '?'
            if 'nick_name' in wxrd:
                item['nick_name'] = wxrd['nick_name']
            data.append(item)
        return data

    def send(self):
        """
        :return: 通过websocket 发送数据到前端
        """
        socketio.emit('req_data', self.get())


def index_gzh(nickname):
    from utils.front import notification
    notification('正在准备搜索工作 请不要关闭WCplus', nickname, 'warning')
    from app.search.index import GZHIndex
    GZHIndex(nickname).index()
    notification('可以开始搜索啦', nickname, 'success')


class Begin2Crawl():
    """
    接受采集范围作为参数 从数据库中读取请求参数执行采集任务
    """
    def __init__(self, filter):
        # 将日期转化为timestamp
        if filter['start_time']:
            filter['start_time'] = datetime.strptime(filter['start_time'].split('T')[0], "%Y-%m-%d").timestamp()
            filter['end_time'] = datetime.strptime(filter['end_time'].split('T')[0], "%Y-%m-%d").timestamp()
        self.filter = filter
        # 记录开始时间
        self.begin_time = time.time()

    def crawler_article_list(self, process):
        """
        :return: 根据数请求参数发起一次文章列表采集
        """
        from app.weixin_crawler.article_list import AricleList
        alc = AricleList()
        alc.get_all_article_list(filter=self.filter, process=process)

    def crawler_reading_data(self, process, mov):
        """
        :return: 根据请求参数发起一次阅读数据采集
        """
        from app.weixin_crawler.reading_data import ReadingData
        rdc = ReadingData()
        rdc.get_all_reading_data(process, mov=mov)

    def crawler_article(self, process):
        """
        :return: 根据请求参数发起一次文章内容采集
        """
        from instance import user_settings
        # 如果不使用代理IP 使用更少的线程数 采集文章正文数据
        use_proxy = user_settings.get()['use_proxy']
        if use_proxy == 'false':
            worker_num = 64
        else:
            worker_num = 8
        debug_p(worker_num)
        from app.weixin_crawler.article import get_all_article
        get_all_article(worker_num=worker_num, process=process)

    @staticmethod
    def article_location2mov(al):
        """
        :return: 将前端的article_location转化为mov
        """
        mov = int(al/10)+10
        if mov > 17:
            mov = 17
        return mov

    def crawl(self):
        from utils.front import message_box
        # 没有参数不采集
        req_data_list = rd.tidy()
        if len(req_data_list)==0:
            return
        nickname = req_data_list[0]['nickname']
        from app.api.process import Process
        crange = int(self.filter['range'])
        mov = self.article_location2mov(int(self.filter['article_location']))
        process = Process(crange)
        # 将process注入builti中全局共享 任何地方都能发送采集状态到前端 重命名为crawler_process
        import builtins
        builtins.crawler_process = process
        if crange == 0:
            process.new_step()
            self.crawler_article_list(process)
            index_gzh(nickname)
        elif crange == 25:
            process.new_step()
            self.crawler_article_list(process)
            process.new_step()
            self.crawler_article(process)
            index_gzh(nickname)
        elif crange == 50:
            process.new_step()
            self.crawler_article_list(process)
            index_gzh(nickname)
            process.new_step()
            self.crawler_reading_data(process, mov)
        elif crange == 75:
            process.new_step()
            self.crawler_article_list(process)
            process.new_step()
            self.crawler_article(process)
            index_gzh(nickname)
            process.new_step()
            self.crawler_reading_data(process, mov)
        elif crange == 100:
            process.new_step()
            self.crawler_reading_data(process, mov)
        # 发送结束信息 使能开始采集按钮
        process.send_finish()
        message_box("总共用时%d分钟"%(int((time.time()-self.begin_time)/60)), "采集完成", "success")




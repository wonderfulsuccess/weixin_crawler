"""
采集进度管理
"""
from utils.base import debug_p


class Process():
    def __init__(self, crange):
        """
        :param range: 采集范围 生成steps
        """
        self.crange = crange
        self.process = {}
        steps = []
        s1 = {
            'title': '采集文章列表',
            'des': '已经采集0篇文章',
            'percent': 0,
            'color': '#ff000'
        }
        s2 = {
            'title': '采集正文',
            'des': '文章数0/0 速度0',
            'percent': 0,
            'color': '#ff00'
        }
        s3 = {
            'title': '采集阅读数据',
            'des': '文章数0/0 速度0',
            'percent': 0,
            'color': '#ff00ff'
        }
        if crange == 0:
            steps.append(s1)
        elif crange == 25:
            steps.append(s1)
            steps.append(s2)
        elif crange == 50:
            steps.append(s1)
            steps.append(s3)
        elif crange == 75:
            steps.append(s1)
            steps.append(s2)
            steps.append(s3)
        elif crange == 100:
            steps.append(s3)
        self.process['steps'] = steps
        self.process['busy'] = 1
        self.process['current'] = 0

    def new_step(self):
        """
        :return: 发送新步骤开始
        """
        from utils.front import notification
        notification(title='采集进入新阶段', message=self.process['steps'][self.process['current']]['title'], _type='success', duration=5)
        self.process['current'] += 1
        self.send_process()

    def new_article_list(self, article_num):
        """
        :param article_num:
        :return: 报告已经采集文章列表的总数
        """
        index = self.process['current']-1
        self.process['steps'][index]['des'] = '已经采集*篇文章'.replace('*', str(article_num))
        self.process['steps'][index]['percent'] = 0
        self.send_process()

    def new_article(self, finished_num, total_num ,proxy_ip, speed):
        """
        :param finished_num: 已经完成的文章数
        :param total_num: 总共需要采集的文章数
        :param proxy_ip: 当前代理ip
        :param speed: 速度
        :return: 采集完以一篇文章后发送进度
        """
        index = self.process['current']-1
        self.process['steps'][index]['des'] = '文章数%d/%d 速度%.3f篇/秒'%(finished_num, total_num, 1.0/speed)
        self.process['steps'][index]['percent'] = round(finished_num/total_num*100, 2)
        self.send_process()

    def new_reading_data(self, finished_num, total_num, delay):
        """
        :param finished_num: 已经采集的文章数
        :param total_num: 文章总数
        :param delay: 采集间隔
        :return: 新采集到阅读数据之后发送进度
        """
        index = self.process['current']-1
        self.process['steps'][index]['des'] = '文章数%d/%d 速度%.3f篇/秒'%(finished_num, total_num, 1.0/delay)
        self.process['steps'][index]['percent'] = round(finished_num/total_num*100, 2)
        self.send_process()

    def send_process(self):
        """
        :return: 通过websocket发送数据
        """
        from web_server import socketio
        socketio.emit('process', self.process)

    def send_finish(self):
        self.process['busy'] = 0
        self.send_process()

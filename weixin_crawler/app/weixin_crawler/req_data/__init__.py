"""
管理请求参数 接受爬虫参数是否过期的指令 提供自动或手动更新参数的方法
全局只有一个实例 参数既可以被动更新 在自动模式之下也可以定时更新
定时更新的好处在于 后台自动更新不用等待 整个采集过程完整
1. 从指定地方库读取参数
2. 整理请求参数
3. 报告请求参数的状态
4. 调用自动获取参数的接口
"""
import json
from datetime import datetime
from instance import col_req_data


class ReqData():
    def __init__(self):
        # 原始数据 组成的list
        self.req_data_list = []
        # 分组之后的数据 组成的list
        self.wx_req_data_list = []

    def clean(self):
        """
        进行数据的初步处理
        1. 从数据源获取原始数据
        2. 基本格式转化
        3. 添加部分字段
        """
        self.req_data_list = []
        raw_data_list = col_req_data.get()
        for rd in raw_data_list:
            item = {}
            item['key'] = rd['key']
            item['time'] = datetime.timestamp(rd['time'])
            # 并不是所有的value都是json格式字符串
            if rd['value'][0] == '{':
                item['value'] = json.loads(rd['value'])
            else:
                item['value'] = rd['value']
            self.req_data_list.append(item)

    def tidy(self):
        """
        :return: 分组 返回一个list 格式如下
        [
            {'nick_name': '微信昵称',
             'nickname': '公众号名称',
             'home': '点击全部消息的主页',
             'load_more': '加载更多历史消息',
             'content': '文章正文',
             'appmsg_comment': '评论',
             'getappmsgext': '阅读数据',},
        ]
        """
        # 找出nickname
        # 找出所有的nick_name
        # 组合该nick_name下的参数
        self.clean()
        nickname = 'UNK'
        wx_req_data_list = []
        wx_req_data_dict = {}
        # 先存储在dict中
        for rd in self.req_data_list:
            item = {}
            # 处理当前的公众号名称
            if rd['key'] == 'current_nickname':
                nickname = rd['value']
            # 处理各个url的请求参数
            elif 'req' in rd['key']:
                keys = rd['key'].split('.')
                if keys[0] not in wx_req_data_dict:
                    wx_req_data_dict[keys[0]] = {}
                wx_req_data_dict[keys[0]][keys[1]] = rd['value']
                wx_req_data_dict[keys[0]][keys[1]]['time'] = rd['time']
            # 处理微信昵称
            elif 'nick_name' in rd['key']:
                keys = rd['key'].split('.')
                if rd['value'] not in wx_req_data_dict:
                    wx_req_data_dict[rd['value']] = {}
                wx_req_data_dict[rd['value']]['nick_name'] = keys[0]
        # 再转化为list
        for key in wx_req_data_dict:
            item = wx_req_data_dict[key]
            item['wxuin'] = key
            item['nickname'] = nickname
            wx_req_data_list.append(item)
        self.wx_req_data_list = wx_req_data_list
        # debug_p(wx_req_data_list)
        return wx_req_data_list

    def delete(self, nick_name, a=False):
        """
        :param a: 是否需要删除公众号的昵称
        :param nick_name: 需要删除的微信昵称
        :return: 删除所有的参数
        """
        # 在Android微信7.0下抓不到月度数据 导致无法删除相关参数 直接全部删除
        if nick_name == '?':
            a = True
        # 删除公众号昵称 意味着全部删除
        if a:
            col_req_data.delete()
            return
        # 删除昵称
        col_req_data.delete(key=nick_name+'.nick_name')
        # 删除wxuin
        wxuin = None
        for wx in self.wx_req_data_list:
            if wx['nick_name'] == nick_name:
                wxuin = wx['wxuin']
                break
        # 删除参数 使用正则表达式匹配 含有特定内容的key
        if wxuin:
            col_req_data.delete(key={'$regex': wxuin+'.*'})

    def check(self):
        """
        :return: 轮训数据源 检查参数的状态 怎么检查呢？
        方便周期性运行 不停检查：
        1. 参与采集微信的数量
        2. 各个参数的采集时间
        """
        pass

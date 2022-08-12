"""
阅读数据爬虫
"""
import requests
from utils.base import debug_p, logger
from copy import copy
from datetime import datetime
from utils.data_process import str_to_dict, dict_to_str,update_dict_by_dict
import time
from instance import stop_and_start

class Crawler():
    def __init__(self, url, comment_id, wx_req_data):
        """
        :param url: 文章的url
        :param wx_req_data: 一个微信的全部请求参数 也就是 wx_req_data_list中的一个
        :return 维护一个请求的请求参数和响应
        """
        # 请求数据
        self.req = {}
        # 响应数据
        self.res = {}
        self.url = url
        self.comment_id = comment_id
        self.wx_req_data = wx_req_data
        # http请求超时时间 秒
        self.timeout = 20
        # 请求是否成功
        self.success = False

    @staticmethod
    def rename_content_url_parm_name(url_parm_dict):
        """
        :param url_parm_dict:
        :return: 重命名微信文章链接参数名称
        """
        name_map = {
            '__biz':'__biz',
            'mid':'mid',
            'idx':'idx',
            'scene':'scene',
            'sn':'sn',
            'appmsgid':'mid',
            'itemidx':'idx',
            'sign':'sn',
            'chksm':'chksm',
        }
        new_parm_dict = copy(url_parm_dict)
        for key in url_parm_dict:
            if key in new_parm_dict:
                new_parm_dict[name_map[key]] = new_parm_dict.pop(key)
        return new_parm_dict


    def prepare_req_data(self):
        """
        :return: 根据url整理请求参数
        """
        # 将url参数转化为字典
        # 用该字典填充请求body参数中的相关字段
        rd = self.wx_req_data['getappmsgext']
        url_parm_dict = str_to_dict(self.url.split('?')[1],'&','=')
        body_dict = str_to_dict(rd['requestData'],'&','=')
        # 修改早期文章的url参数名称
        new_url_parm_dict = self.rename_content_url_parm_name(url_parm_dict)
        body_dict['is_need_reward'] = 1
        update_dict_by_dict(body_dict,new_url_parm_dict,['mid','sn','idx','scene'])
        # 为了获取评论数 修改comment_id
        body_dict['comment_id'] = self.comment_id
        # 需要赞赏数量
        body_dict['is_need_reward'] = 1
        # 修改请求参数
        self.req['url'] = rd['url']
        self.req['body'] = dict_to_str(body_dict)
        self.req['headers'] = rd['requestOptions']['headers']

    def act_request(self):
        """
        :return: 执行请求 如果请求失败返回字符串"error"
        """
        resp = None
        proxy_err_cnt = 0
        while not resp:
            # 请求发生异常次数过多 放弃
            if proxy_err_cnt >= 3:
                logger.warning("获取历史文章阅读数据发生错误%s 次数太多 放弃"%(self.url))
                return 'error'
            try:
                resp = requests.post(
                    url=self.req['url'],
                    data=self.req['body'],
                    headers=self.req['headers'],
                    timeout=self.timeout,
                    verify=True)
            except Exception as e:
                proxy_err_cnt += 1
                logger.warning("获取文章阅读数据发生错误 5秒钟之后再次尝试 %s %s"%(self.url, str(e)))
                time.sleep(5)
        return resp

    def jude_request(self, resp):
        """
        :return: 判断请求是否成功 如果不成功 直接采集相关措施
        比如重新请求 或者操作手机获取参数
        """
        # 返回一个None
        if resp == "error":
            logger.error('请求失败, 未能获取到阅读数据')
            self.success = False
            return None
        resp_json = resp.json()
        # 正常
        if 'appmsgstat' in resp_json:
            # 通过安检
            stop_and_start.check({'crawler':'阅读数据', 'msg':'success'})
            self.success = True
            return resp
        # 请求频繁
        # elif 'errmsg' in resp_json['base_resp']:
        #     debug_p(resp_json)
        #     logger.warning("获取文章阅读数据频繁等待5分钟之后继续 %s"%(self.url))
        #     time.sleep(5*60)
        #     self.jude_request(self.act_request())
        # 参数过期 {'advertisement_info': [], 'reward_head_imgs': []}
        else:
            logger.error("请求阅读数据参数错误 %s"%(self.url))
            self.success = False
            return None

    def decode_response(self, resp):
        """
        :return: 解析响应返回成为原始数据
        """
        read_data = DecodeReadingData.decode_read_data(resp)
        return read_data

    def run(self):
        """
        :return: 运行所有的过程
        """
        self.prepare_req_data()
        resp = self.jude_request(self.act_request())
        # 请求成功才需要解析数据
        if self.success:
            read_data = self.decode_response(resp)
            return read_data
        # 否则返回None告诉上层 需要处理后重新操作
        else:
            return 'req_data_error'


class DecodeReadingData():
    @staticmethod
    def decode_read_data(response):
        rj = response.json()
        read_data = {}
        read_data['read_num'] = rj.get("appmsgstat").get("read_num")
        read_data['like_num'] = rj.get("appmsgstat").get("like_num")
        read_data['reward_num'] = rj.get("reward_total_count")
        # read_data['nick_name'] = rj.get("nick_name")#  已登陆的微信名称
        if read_data['read_num'] is None:
            read_data['read_num'] = -2
        if read_data['like_num'] is None:
            read_data['like_num'] = -2
        if read_data['reward_num'] is None:
            read_data['reward_num'] = -2
        read_data['c_date'] = datetime.now()
        read_data['comment_num'] = rj.get("comment_count")
        if read_data['comment_num'] is None:
            read_data['comment_num'] = -2
        DecodeReadingData.print_log(read_data)
        return read_data

    @staticmethod
    def print_log(rd):
        # 准备任务日志信息
        logger.info('采集阅读数据中... 阅读%-5d 点赞%-4d 赞赏%3d 评论%d'%(rd['read_num'], rd['like_num'], rd['reward_num'], rd['comment_num'] ))

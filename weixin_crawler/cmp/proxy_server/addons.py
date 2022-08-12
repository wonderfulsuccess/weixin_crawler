"""
自定义mimproxy脚本 详细见 https://docs.mitmproxy.org/stable/addons-overview/
由于使用anyproxy的历史原因 这里会解析mitmproxy代理数据为anyproxy同样的格式
"""
import json
from utils.data_process import str_to_dict
from utils.base import logger, debug_p
from datetime import datetime
from instance import col_req_data
# 保存当前会话的wxuin
wxuin = None

url_filter = {
    "load_more":"https://mp.weixin.qq.com/mp/profile_ext?action=getmsg",            #更多历史消息
    "getappmsgext":"https://mp.weixin.qq.com/mp/getappmsgext?",                     #阅读消息
    "appmsg_comment":"https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment",#评论信息
    # content url 发生变化
    "content":"https://mp.weixin.qq.com/s?",                                        #文章正文html
    "home":"https://mp.weixin.qq.com/mp/profile_ext?action=home"                    #历史消息home
}

def insert_helper(key, value):
    # 单引号转化为双引号 方便使用json函数转数据为dict类型
    json_value = str(value).replace("'",'"')
    data = {'id':key,'key':key,'time':datetime.now(),'value':json_value}
    col_req_data.insert('id', data)


class SelfAddon:
    """
    拦截url_filter中的请求参数 用wxuin.key.req的格式作为key name 存入数据库
    """
    @staticmethod
    def _extract_wxuin(req_data):
        """
        :param req_data:
        :return: 微信特有 从cookie中解析出wxuin
        """
        wxuin = 'UNK'

        # 某次微信接口升级 headers中的cookie变成大写Cookie
        if 'Cookie' in req_data['requestOptions']['headers']:
            cookie_dict = str_to_dict(req_data['requestOptions']['headers']['Cookie'],';','=')
        else:
            cookie_dict = str_to_dict(req_data['requestOptions']['headers']['cookie'],';','=')

        if 'wxuin' in cookie_dict:
            wxuin = cookie_dict['wxuin']
        return wxuin


    def request(self, flow):
        pass

    def response(self, flow):
        # 检查是否是过滤器中的url
        for key in url_filter:
            if url_filter[key] in flow.request.url:
                # 请求参数进行格式转化 得到请求参数和时间戳
                req_data,timestamp = ExtractFlow.format_request_data(flow.request)
                # debug_p(req_data)
                global wxuin
                if key == 'home':
                    wxuin = self._extract_wxuin(req_data)
                # 没有获取到微信昵称不保存参数
                if wxuin == 'UNK':
                    return
                key_name = '%s.%s.req'%(wxuin, key)
                insert_helper(key_name,req_data)
                logger.debug(key_name)
                # 获取当前微信的昵称和微信的wxuin 以此支持多微信同时采集
                if key == 'getappmsgext':
                    # 找出当前微信昵称
                    status_code,text = ExtractFlow.get_response(flow.response)
                    text_dict = json.loads(text)
                    nick_name = 'UNK'
                    if 'nick_name' in text_dict:
                        nick_name = text_dict['nick_name']
                        if nick_name == 'UNK':
                            logger.debug('没能找到微信昵称 换一篇文章点击试试看 确保文章底部阅读数据出现')
                        else:
                            insert_helper(nick_name+'.nick_name', wxuin)

                elif key == 'home':
                    status_code, html_text = ExtractFlow.get_response(flow.response)
                    current_nickname = html_text.split('var nickname = "')[1].split('" || ""')[0]
                    logger.info('准备公众号:'+current_nickname)
                    insert_helper('current_nickname',current_nickname)


class ExtractFlow():
    """
    解析flow数据 成为anyrpoxy格式
    """
    @staticmethod
    def format_request_data(request):
        """
        :param request:
        :return: 模拟anyrpoxy 格式化请求数据
        """
        req_data = {}
        req_data["protocol"] = request.scheme
        req_data["url"] = request.url
        req_data["requestOptions"] = {}

        req_data["requestOptions"]["headers"] = ExtractFlow.decode_headers(request.headers)
        req_data["requestOptions"]["hostname"] = request.pretty_host
        req_data["requestOptions"]["port"] = request.port
        req_data["requestOptions"]["path"] = request.path
        req_data["requestOptions"]["method"] = request.method

        req_data["requestData"] = request.text

        timestamp = int((request.timestamp_end)*1000)
        return req_data, timestamp

    @staticmethod
    def get_response(response):
        """
        :param response:
        :return: 返回响应码和响应体
        """
        return response.status_code, response.text

    @staticmethod
    def decode_headers(headers):
        headers_data = {}
        for i in headers.fields:
            headers_data[str(i[0],'utf-8')] = str(i[1],'utf-8')
        # headers中出现了一个不明字段 会导致request出错
        if ':authority' in headers_data:
            headers_data.pop(':authority')
        return headers_data

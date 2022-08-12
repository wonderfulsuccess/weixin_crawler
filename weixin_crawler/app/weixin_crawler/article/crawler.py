"""
文章正文爬虫
"""

class Aricle():
    def __init__(self, url, proxy):
        """
        :param url: 文章的url
        :param proxy: 代理ip
        :return 维护一个请求的请求参数和响应
        """
        # 请求数据
        self.req = {}
        # 响应数据
        self.res = {}
        pass

    def act_request(self):
        """
        :return: 执行请求
        """
        pass

    def jude_request(self):
        """
        :return: 判断请求是否成功 如果不成功 直接采集相关措施
        比如重新请求 或者操作手机获取参数
        """
        pass

    def decode_response(self):
        """
        :return: 解析响应返回成为原始数据
        """
        pass

    def run(self):
        """
        :return: 运行所有的过程
        """
        pass


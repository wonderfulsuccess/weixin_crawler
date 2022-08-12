"""
管理所有的爬虫
1. 利用rq对象统从数据源或请求参数 为了减少数据库操作的频率 缓存该数据
"""
import time

class Stop():
    """
    管理爬虫的暂停或启动 每种爬虫的最频繁动作都会调用它的某个方法
    该方法要么一直卡壳直到满足某种状态 要么直接放行
    他是一个岗哨或者是一个检查站 会被设置在流量入口 通过token验证对方的状态
    岗哨还要能接受外部的指令 可改变通行规则

    更多的规则陆续加入
    """
    def __init__(self):
        # 全局检查 是否暂停采集
        self.pause = False

    def stop(self):
        self.pause = True

    def start(self):
        self.pause = False

    def check(self, token):
        """
        :param token: {'crawler':'爬虫名称', 'msg':'judge返回的结果'}
        :return: 安置在流量入口 通过对方的token和本身的规则决定是否放行
        如果不能放行 根据对方不能通过的原因 主动处理异常（重新获取参数）或者等待更新放行规则（比如从暂停中恢复采集）
        """
        # 第1岗 检查是否全局暂停 为了降低CPU使用率 每隔一段时间再检查
        while self.pause:
            time.sleep(0.1)
        # 第2岗 检查judge的返回状态 检查参数是否错误 设置为stop 参数更新之后由别的程序设置为start状态
        if token['msg'] == 'req_data_error':
            self.pause = True
            from utils.front import message_box
            message_box("需要重新操作当前公众号 获取参数"+token['crawler'], "参数错误", "error")
            # 暂停等待 其它程序调用 start()
            # from web_server import socketio
            # socketio.emit('pause', 1)
            while self.pause:
                time.sleep(0.1)

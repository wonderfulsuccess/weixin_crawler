"""
定义全局对象
"""
from cmp.db.mongo import CollectionOperation
# 采集日志操作
col_crawler_log = CollectionOperation('crawler_log')
# 请求参数据库操作实例
col_req_data = CollectionOperation('req_data')
# 收藏数据库操作实例
col_like = CollectionOperation('微搜收藏')

# 请求参数管理实例
from app.weixin_crawler.req_data import ReqData
rd = ReqData()

# 用户设置实例
from app.api.settings import Settings
user_settings = Settings()

# 采集启停
from app.weixin_crawler import Stop
stop_and_start = Stop()

# 发送到印象笔记
# try:
#     from app.send_evernote import Send2Evernote
#     send_ervernote = Send2Evernote()
#     send_ervernote.set_device()
# except:
#     send_ervernote = None

from utils.base import the_platform
PLATFORM = the_platform()

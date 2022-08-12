from flask import Flask
from flask_socketio import SocketIO
from flask_restful import Api
# 允许跨域请求
from flask_cors import CORS
import logging
from utils.base import logger

# 禁止一般性的日志打印
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# 定义web实例
web_app = Flask('WCplus', template_folder="./web_server/static", static_folder="./web_server/static")

# 允许跨域请求
CORS(web_app, resources={r"/api/*": {"origins": "*"}})

# 挂载api 注入API rest api 都在/api 路由之下
from web_server.api import api_resources
api = Api(web_app)
for item in api_resources:
    api.add_resource(item['res'], '/api'+item['url'])


# 定义websocket对象 websocket 通信通过该对象实现
socketio = None
# Mac的生产环境并不不能直接使用gevent模式 防止错误发生
try:
    socketio = SocketIO(web_app, async_mode='gevent', log_output=False)
    logger.info('Gevent server mode')
except:
    socketio = SocketIO(web_app, log_output=False)
    logger.warning('Threading server mode')

# 加载路由
from web_server.router import *


# 加载事件
from web_server.event import *


def run_webserver():
    socketio.run(web_app, host= '0.0.0.0', port=5000)

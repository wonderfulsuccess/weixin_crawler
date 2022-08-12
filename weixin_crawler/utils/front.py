"""
前端相关的一些方法 不能单独在web中使用需要web服务和相关前端代码的配合
"""


def message(message, _type=''):
    """
    :param _type: 默认 success warning error
    :param message:
    :return: 顶部下拉消息
    """
    from web_server import socketio
    socketio.emit('message', {'type':_type, 'message':message})


def message_box(message, title, _type=''):
    """
    :param message:默认 success warning error
    :param title:
    :param _type:
    :return: 弹窗消息
    """
    from web_server import socketio
    socketio.emit('message_box', {'message':message, 'title':title, 'type':_type})


def notification(message, title, _type='', duration=3):
    """
    :param message:默认 success warning error
    :param title:
    :param _type:
    :param duration: 消息显示时间 0表示消息不会自动关闭
    :return: 右侧消息
    """
    from web_server import socketio
    socketio.emit('notification', {'message':message, 'title':title, 'type':_type, 'duration':duration})


def command_log(item):
    """
    :param item:
    :return: 发送一条日志
    """
    from web_server import socketio
    socketio.emit('command', item)

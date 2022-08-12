"""
websocket事件监听
"""
from web_server import socketio


@socketio.on('connect')
def handle_message_connected():
    socketio.emit('connect',{'data':'hand shake'})


@socketio.on('hello')
def handle_hello(data):
    # 如果数据中有汉字 可能是乱码 通过以下方式解码
    # data['某个value为字符串的key'].encode(encoding='raw_unicode_escape').decode("utf-8"),
    print(data)


@socketio.on('pause')
def handle_pause(data):
    # 如果数据中有汉字 可能是乱码 通过以下方式解码
    # data['某个value为字符串的key'].encode(encoding='raw_unicode_escape').decode("utf-8"),
    from instance import stop_and_start
    if data:
        stop_and_start.stop()
    else:
        stop_and_start.start()


@socketio.on('ask_data')
def handle_ask_data(data):
    # 请求发送请求参数
    if data == 'req_data':
        from app.api.crawler import ReqData
        ReqData().send()
    # 发送爬虫状态 采集状态会被放在builtins模块中 全局共享
    try:
        import builtins
        builtins.crawler_process.send_process()
    except:
        pass


@socketio.on('export_excel')
def handle_export_excel(nickname):
    nickname = nickname.encode(encoding='raw_unicode_escape').decode("utf-8")
    from app.export.excel import ExportExcel
    ExportExcel(nickname).run()


@socketio.on('delete_gzh')
def handle_delete_gzh(nickname):
    nickname = nickname.encode(encoding='raw_unicode_escape').decode("utf-8")
    from app.api.delete import DeleteGZH
    DeleteGZH(nickname).run()


@socketio.on('command')
def handle_command(command):
    command = command.encode(encoding='raw_unicode_escape').decode("utf-8")
    from app.command_handler import execute_command
    execute_command(command)

# @socketio.on('send_evernote')
# def handle_send_evernote(content_url_list):
#     from instance import send_ervernote
#     if send_ervernote:
#         for url in content_url_list:
#             send_ervernote.add_task(url)
#         send_ervernote.run()
#     else:
#         print('没找到手机')


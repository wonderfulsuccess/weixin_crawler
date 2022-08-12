"""
一个命令对应该模块下的一份python文件
注册时指定命令和处理模块
"""
# import 命令处理器
from app.command_handler.index_all_gzh import IndexAllGZH
from app.command_handler.utils_cmd import MovStr2Int
# 注册命令和对应的处理器
commands = {
    'index all gzh': IndexAllGZH(),
    'mov str to int': MovStr2Int()
}


def execute_command(command):
    """
    :param command:
    :return: 参数使用 ' - ' 间隔
    """
    from utils.front import notification
    cmd = command.split(' - ')[0]
    cmd_args = command.split(' - ')[1:]
    if cmd not in commands:
        notification(command, '不支持的命令', _type='error')
    else:
        notification(command, '开始执行', _type='success')
        # 线程背后运行
        from threading import Thread
        Thread(target=commands[cmd].run, args=(cmd, cmd_args)).start()

def get_ip():
    """
    :return: 获取局域网IP地址
    """
    from instance import PLATFORM
    if PLATFORM == 'win':
        import socket
        ip = socket.gethostbyname(socket.gethostname())
        return ip
    elif PLATFORM == 'osx':
        return '终端运行 ifconfig 查看'

        
if __name__ == '__main__':
    print(get_ip())

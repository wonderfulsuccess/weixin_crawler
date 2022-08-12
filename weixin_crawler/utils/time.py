def get_internet_time():
    """
    :return: 获取百度服务器时间
    """
    import requests,time,datetime
    try:
        r = requests.get(url="http://www.baidu.com")
        date = r.headers['Date']
        #将GMT时间转换成北京时间
        net_time = time.mktime(datetime.datetime.strptime(date[5:25], "%d %b %Y %H:%M:%S").timetuple())+8*3600
        return int(net_time)
    except:
        from instance import PLATFORM
        if PLATFORM == 'win':
            return None
        else:
            import time
            return (time.time())

if __name__ == '__main__':
    net_time = get_internet_time()
    if net_time:
        print(net_time)

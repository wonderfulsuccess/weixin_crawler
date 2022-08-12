"""
提供代理IP
"""
import requests,time
from instance import user_settings
from utils.base import logger
from utils.front import message_box


def get_proxy_ip(source=0):
    """
    :param source:0使用付费的芝麻IP 1使用开源的proxypool
    :return: 以字符串的形式返回一个IP 例如 171.13.149.40:26632
    """
    proxy = charge_proxy()
    return proxy


def charge_proxy():
    # 读取代理IP URL
    settings = user_settings.get()
    print(settings)
    if 'proxy' in settings:
        ip_url = settings['proxy']
    else:
        logger.logger('请先设置代理IP')
        message_box('没有设置代理IP请先设置 设置之后请验证 确保返回的只有一个代理IP 例如 123.234.345.12:9808', '代理设置', 'error')
        return '127.0.0.1:1080'
    try:
        r_text = requests.get(ip_url).text
        if "白名单" in r_text:
            message_box('即将使用真实IP'+r_text, '获取代理IP出错', 'error')
            time.sleep(1)
            return '127.0.0.1:1080'
    except:
        message_box('请设置正确的代理IP 设置后请验证保证可返回一个代理IP 如果真实IP可用将使用真实IP进行采集', '代理设置', 'error')
        return '127.0.0.1:1080'
    while "请求" in r_text:
        time.sleep(1)
        print('等待返回代理IP...')
        r_text = requests.get(ip_url).text
    return r_text


if __name__ == '__main__':
    print(get_proxy_ip(1))

"""
代理服务器模块
"""
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
# 自定义代理逻辑
from cmp.proxy_server.addons import SelfAddon


def start_proxy():
    self_addon = SelfAddon()
    opts = options.Options(listen_host='0.0.0.0', listen_port=8080)
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(self_addon)
    # 找到IP地址
    # import socket
    # ip = socket.gethostbyname(socket.gethostname())
    # print("请设置手机代理IP:"+str(ip)+"端口:8080")
    try:
        m.run()
    except KeyboardInterrupt:
        print("")
        m.shutdown()


if __name__ == "__main__":
    start_proxy()

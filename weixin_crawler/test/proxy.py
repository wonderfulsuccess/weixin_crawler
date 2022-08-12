import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

url = "http://mp.weixin.qq.com/s?__biz=MjM5NzcwNzU5MQ==&mid=2662633911&idx=2&sn=efdae85aeb27eabb6cb8a5d403edc32d&chksm=bd95db9f8ae252892970797c94fe6b83bcd87cda5f3019d9cf38b9c529b37dc837afa82ae585&scene=27#wechat_redirect"

proxies = {"http":'112.85.126.18:4216',"https":'112.85.126.18:4216'}

if __name__ == '__main__':
    r = requests.get(url = url,
                     headers = headers,
                     timeout = 20)
    print(r.text)

from flask_restful import Resource, reqparse


# 注册需要解析的URL参数
parser = reqparse.RequestParser()
arguments = ['range', 'type', 'num', 'start_time', 'end_time', 'nick_name','article_location']
for arg in arguments:
    parser.add_argument(arg)


class Crawler(Resource):
    def get(self):
        pass

    def post(self):
        from app.api.crawler import Begin2Crawl
        from threading import Thread
        args = parser.parse_args()
        Thread(target=Begin2Crawl(args).crawl).start()

    def delete(self):
        from instance import rd
        nick_name = parser.parse_args()['nick_name']
        rd.delete(nick_name)



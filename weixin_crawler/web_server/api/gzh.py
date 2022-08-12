from flask_restful import Resource, reqparse


# 注册需要解析的URL参数
parser = reqparse.RequestParser()
arguments = ['nickname', 'type', 'start', 'end', 'mov']
for arg in arguments:
    parser.add_argument(arg)


class GZH(Resource):
    def get(self):
        from app.api.gzh import Finished
        return Finished().get()

    def post(self):
        args = parser.parse_args()
        from app.api.gzh import Finished
        # 有些公众号的数据非常多 仅支持对主文章进行排序
        if args['mov'] == '10':
            articles = Finished().get_article_list(page_info=args, mov=10)
        else:
            articles = Finished().get_article_list(page_info=args)
        return articles


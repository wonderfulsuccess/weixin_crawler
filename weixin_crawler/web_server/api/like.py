from flask_restful import Resource, reqparse
from app.api.like import MyLike
from utils.base import debug_p


# 注册需要解析的URL参数
parser = reqparse.RequestParser()
arguments = ['nickname', 'content_url', 'start', 'end']
for arg in arguments:
    parser.add_argument(arg)


class MyLikeAPI(Resource):
    def get(self):
        """
        :return: 获取收藏列表 start end
        {'total':0,
         'articles':[]}
        """
        args = parser.parse_args()
        data = MyLike.get_like_info()
        data['articles'] = MyLike.get_like_list({'start':int(args['start']), 'end':int(args['end'])})
        return data

    def post(self):
        """
        :return: 添加到收藏列表 nickname content_url
        """
        args = parser.parse_args()
        MyLike.add_like(args)

    def delete(self):
        """
        :return: 从列表中删除content_url
        """
        args = parser.parse_args()
        MyLike.delete_like(args)

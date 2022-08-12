from flask_restful import Resource, reqparse
from instance import user_settings
# 注册需要解析的URL参数
parser = reqparse.RequestParser()
arguments = ['proxy', 'use_proxy', 'article_list_delay', 'reading_data_delay', 'save_html']
for arg in arguments:
    parser.add_argument(arg)


class Settings(Resource):
    def get(self):
        return user_settings.get()

    def put(self):
        args = parser.parse_args()
        user_settings.insert(args)

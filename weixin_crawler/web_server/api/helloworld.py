from flask_restful import Resource, reqparse


# 注册需要解析的URL参数
parser = reqparse.RequestParser()
arguments = ['name', 'age']
for arg in arguments:
    parser.add_argument(arg)


class HelloWorld(Resource):
    def get(self):
        return {'name': 'frank', 'age': 18}

    def post(self):
        args = parser.parse_args()
        print(args)

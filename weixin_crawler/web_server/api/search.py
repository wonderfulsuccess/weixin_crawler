from flask_restful import Resource, reqparse


# 注册需要解析的URL参数
parser = reqparse.RequestParser()
# 搜索的公众号 搜索关键词 搜索字段 开视页 数量
arguments = ['range', 'search_data', 'fields', 'from', 'size']
for arg in arguments:
    parser.add_argument(arg)


class Search(Resource):
    def get(self):
        """
        :return: 打开搜索页 返回可用的搜索信息
        """
        from app.api.search import index_info
        return index_info()

    def post(self):
        """
        :return: 返回搜索的结果
        1标题 2摘要 3文章 4全部
        """
        args = parser.parse_args()
        # 修改fields
        if args['fields'] == '1':
            args['fields'] = ['title']
        elif args['fields'] == '2':
            args['fields'] = ['digest']
        elif args['fields'] == '3':
            args['fields'] = ['article']
        else:
            args['fields'] = ['title', 'digest', 'article']
        # 修改搜索公众号的范围
        if args['range'] == '全部':
            args['range'] = 'gzh_*'
        else:
            args['range'] = 'gzh_'+args['range']
        from app.search.search import GZHSearch
        try:
            result = GZHSearch(search_data=args['search_data'],
                               gzhs=args['range'],
                               fields=args['fields'],
                               _from=int(args['from']),
                               _size=int(args['size'])).get_result()
            return result
        except:
            from utils.base import logger
            logger.warning('搜索请求超时 建议多次尝试')
            return '搜索请求超时 建议多次尝试'

"""
即用即创建 不永久驻留在内存中 专门为公众号数据搜索建立的类 主要完成如下几项工作
输入：搜索关键词（含有搜索规则） 搜索字段范围 公众号（index）范围

输入来来自前端返回的数据
每次搜索都创建一个对象

"""
from cmp.db.es.search import Search


class GZHSearch():
    def __init__(self, search_data, gzhs='*', _from=0, _size=10, fields = ['title', 'article', 'digest']):
        """
        :param search_data: 带有搜索规则的关键字
        :param gzhs: 搜索的公众号范围列表
        :param in_range: 搜索的字段
        :param _from: 结果起始
        :param _size: 返回的数量
        :param fields: 搜索的范围
        """
        self.search_data = search_data
        self.gzhs = gzhs
        self.fields = fields
        self.from_size = {'from':_from, 'size':_size}

    def get_result(self):
        """
        :return: 根据参数设定返回搜索结果
        """
        s = Search(search_data=self.search_data, index_list=self.gzhs, fields=self.fields, from_size=self.from_size)
        return s.search()

    @staticmethod
    def get_all_index_info():
        """
        :return: 获取es中可用索引
        """
        from app.search.index import GZHIndex
        from cmp.db.es.index import IndexDoc
        index_list = GZHIndex.get_all_indices('gzh_*')
        index_info = []
        for index in index_list:
            nickanme = index.split('_')[-1]
            doc_num = IndexDoc(index, doc_type='gzh_article').count()
            index_info.append([nickanme, doc_num])
        return index_info

if __name__ == '__main__':
    data = GZHSearch.get_all_index_info()
    print(data)

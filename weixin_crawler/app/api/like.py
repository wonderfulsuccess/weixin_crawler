"""
为收藏提供数据支撑和功能支撑
"""
from instance import col_like
from cmp.db.mongo import CollectionOperation
from utils.base import debug_p
from datetime import datetime


class MyLike:
    """
    collection的名称叫做"微搜收藏"
    es index 叫做 gzh_微搜搜藏
    """
    def __int__(self):
        """
        检查有没有给索引和数据collection 没有就创建
        """
        pass

    @staticmethod
    def get_like_info():
        """
        :return: 返回搜藏文章的概要信息 : 文章总数 {"total"}
        """
        data = {}
        data['total'] = col_like.count()
        return data

    @staticmethod
    def get_like_list(page_info):
        """
        :param page_info: {'start', 'end'}
        :return: 获取搜藏文章列表 带有分页切片 返回一个[]
        """
        data = []
        data_gen = col_like.get()[page_info['start']:page_info['end']]
        counter = 0
        for d in data_gen:
            counter += 1
            d.pop('_id')
            d['id'] = counter
            d['c_date'] = datetime.now().timestamp()
            if 'c_data' in d:
                d['c_date'] = d['c_date'].timestamp()
            d['like_time'] = d['like_time'].timestamp()
            d['p_date'] = d['p_date'].timestamp()
            data.append(d)
        return data

    @staticmethod
    def add_like(article_info):
        """
        :param article_info: {nickname, content_url}
        :return: 添加到搜藏
        """
        # 根据nickname和url从数据库中获得原始记录
        col_data = CollectionOperation(article_info['nickname'])
        article_data = col_data.get(content_url=article_info['content_url'])[0]
        # 原始数据库中增加已经搜藏字段
        article_data['like_folder'] = True
        col_data.insert(key='content_url', data=article_data)
        # 增加收藏时间
        article_data['like_time'] = datetime.now()
        # 插入 "微搜收藏"
        res = col_like.insert(key='content_url', data=article_data)

    @staticmethod
    def delete_like(article_info):
        """
        :param article_info:{content_irl}
        :return: 删除搜藏
        """
        # 从喜欢列表中删除
        col_like.delete(content_url=article_info['content_url'])
        # 将原始数据库的like记录改为FALSE
        col_data = CollectionOperation(article_info['nickname'])
        article_data = col_data.get(content_url=article_info['content_url'])[0]
        article_data['like_folder'] = False
        col_data.insert(key='content_url', data=article_data)

    @staticmethod
    def index_like():
        """
        :return: 为所有的搜藏文章建立索引 准备搜索
        """
        pass

    @staticmethod
    def search_like(search_data, from_size, fidles):
        """
        :param search_data: 搜索的关键字
        :param from_size:  其实位置和页面size
        :param fidles: 搜索字段
        :return: 调用搜索接口 搜索搜藏列表
        """
        from cmp.db.es.search import Search
        pass

if __name__ == '__main__':
    my_like =  MyLike.get_like_list({'start':0, 'end':1})
    debug_p(my_like)

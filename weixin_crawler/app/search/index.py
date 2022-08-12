"""
文章建立索引的情况
1. 采集阶段 第一次采集完成
2. 采集阶段 更新采集过的公众号

1 处理流程：
0: 先检查该公众号是否存在索引如果索引存在计算文章的数量 以此判断到底应该准备多少公众号的文章
a：从数据库中读取出该公众号的全部数据
b：冲html文件夹中读取所有的html文档 解析成为内容文本
c：解析出html中的文本，组成完整的文章数据
d：数据写入es es根据id跳过已经存在的文档

2 处理流程
处理逻辑和1 一样遇到更新就直接跳出

更新的几种情况
1. 阅读数据更新
2. 文章内容从无到有

索引发生在什么情况下？
情况1 一个公众号采集完毕之后，需要准备索引的速度足够快 创建GZHIndex对象 调用index方法
情况2 一个公众号的数据更新之后，需要准备索引数据的速度足够快 创建GZHIndex对象 调用index方法
情况3 对于3.0 已经采集的数据建立索引 先将html文档解析成文本放入数据库 再调用 index方法
"""
from cmp.db.mongo import CollectionOperation
from app.search.config import doc_schema
from utils.base import logger
from cmp.db.es.index import IndexDoc
import time


class GZHIndex:
    index_prefix = 'gzh_'
    doc_type = 'gzh_article'

    def __init__(self, nickname):
        self.nickname = nickname.lower()
        self.nickname_raw = nickname

    def index_check(self):
        """
        :return: 检查该index是否存在
        """
        return IndexDoc.index_exist(self.nickname)

    @staticmethod
    def get_all_indices(patton=None):
        """
        :param patton: 支持通配符
        :return: 所有加入index的文档和文档数量
        """
        return IndexDoc.get_all_indices(patton)


    def prepare_docs(self, num=None):
        """
        :param num: 如果是具体数字则 准备最近发布的num篇文章
        :return: 根据公众号的昵称准备该公众号的所有或者前n篇文章的全部数据 如果某些字段没有就使用默认值
        """
        from pymongo import DESCENDING
        doc_list = []
        # 从数据库中找出文章列表
        col = CollectionOperation(self.nickname_raw)
        if num:
            db_docs = col.table.find().sort("p_date", DESCENDING)()[:num]
        else:
            db_docs = col.get()
        begin_time = time.time()
        # 根据 doc_schema 中 key 构建doc list
        for doc in db_docs:
            item = {}
            doc['id'] = doc['content_url']
            for key in doc_schema:
                if key in doc:
                    item[key] = doc[key]
                # 如果数据库中没有该字段使用-2填充
                else:
                    item[key] = -2
            doc_list.append(item)
        logger.info('解析文章文本用时 %.3f'%(time.time()-begin_time))
        return doc_list

    def index(self, num=None):
        """
        :param num: 需要冲数据库中挑选出的文章数量
        :return: 用最有效率的方式将文档index到es中
        如果index_check之后的结果和数据库中的文档数量一致 直接跳过 不index
        如果数据和结果不一样 全文再次更新索引
        """
        doc_list = self.prepare_docs(num=num)
        index_doc = IndexDoc(self.index_prefix+self.nickname, doc_list, self.doc_type)
        index_doc.create_index()
        index_doc.index_bulk()

    def delete(self):
        """
        :return: 删除该index
        """
        IndexDoc.delete_index(self.index_prefix+self.nickname)

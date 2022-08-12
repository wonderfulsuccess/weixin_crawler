"""
作为一个通用的index组件 应该是什么样的？
提供文档类型 和一个文档list就够了
index相当于table 文档相当于数据
每个文档一定要有一个id字段 建议使用文章的url
"""
from app.search.config import doc_schema
from cmp.db.es import es_instance
from elasticsearch import helpers
from utils.base import logger


class IndexDoc():
    def __init__(self, index_name, doc_list=None, doc_type = 'articles'):
        """
        :param index_name: index的名称
        :param doc_list:文档列表
        """
        self.index_name = index_name
        self.docs = doc_list
        self.doc_type = doc_type

    def create_index(self):
        """
        :return: 创建index 如果已经存在则不创建
        返回是创建还是已经存 create index 实际上是告诉 es 哪些需要索引 哪些不需要索引
        """
        mapping_body = {}
        mapping_body['properties'] = doc_schema
        exists = es_instance.indices.exists(self.index_name)
        if exists is False:
            es_instance.indices.create(self.index_name)
            es_instance.indices.put_mapping(index=self.index_name, doc_type=self.doc_type, body=mapping_body)
            logger.debug('创建index %s 成功'%(self.index_name))
        else:
            logger.debug('index %s 已经存在'%(self.index_name))
        return exists

    @staticmethod
    def delete_index(index_name):
        """
        :param:指定index的匹配模式 支持通配符* 通过list指定多个index
        :return:删除index和该index下的所有doc
        """
        es_instance.indices.delete(index_name)

    @staticmethod
    def get_all_indices(patton=None):
        """
        :param patton: 支持通配符 *
        :return:
        """
        index_list = []
        # 给出的匹配模式可能找不到index
        try:
            alias = es_instance.indices.get_alias(patton)
        except:
            alias = []
        for key in alias:
            index_list.append(key)
        return index_list

    @staticmethod
    def index_exist(index_name):
        """
        :param index_name:
        :return: 检查index是否存在
        """
        return es_instance.indices.exists(index_name)

    def index_docs(self):
        """
        :return: 索引文档 使用bulk操作
        """
        pass

    def index_doc(self, doc):
        """
        :param doc:文档体
        :return:新建或者更新doc
        """
        # 只对 doc_schema 中定义的字段进行索引
        part_doc = dict((key, doc[key]) for key in doc_schema)
        # 当公众号文章更新之后还产生新的文章 直接跳过对旧有文章的index
        if self.doc_exist(doc['id']) == 1:
            return
        try:
            es_instance.index(index=self.index_name, doc_type=self.doc_type, id=doc['content_url'], body=part_doc)
        except:
            logger.error('index 文档失败 %s'%(doc['title']))

    def index_bulk(self):
        """
        :param index_name: es中的index名称
        :return:使用bulk进行批量index API会根据指定的_id字段去重 而且支持更新 index文档建议优先使用该API
        用id跟踪一篇文章 其余字段变化都是跟新模式 id变化则插入新文档
        """
        actions = []
        for doc in self.docs:
            action = {
                "_index": self.index_name,
                "_type": self.doc_type,
                "_id": doc['id'],
                "_source": doc
            }
            actions.append(action)
        result = helpers.bulk(es_instance, actions)
        return result

    def doc_exist(self, id):
        """
        :param id: 文档id 一般使用文章的url
        :return:文档存在返回1 文档不存在返回0
        """
        # 使用文章的连接判断文档存在与否 存在数量为1 不存在数量为0
        try:
            body = {
                "query":{"match_phrase":{'id': id}},
            }
            result = es_instance.count(index=self.index_name, doc_type=self.doc_type, body=body)['count']
        # 如果公众号对应的index不存在则发生错误 也就说明该文章并未被创建索引
        except :
            result = 0
        return result

    def delete_doc(self, id):
        """
        :param nickname:
        :param url:
        :return: 根据id删除文档
        """
        es_instance.delete(index=self.index_name, doc_type=self.doc_type, id=id)

    def count(self):
        """
        :return: get index doc num
        """
        try:
            body = {
                "query":{"match_all":{}},
            }
            result = es_instance.count(index=self.index_name, doc_type=self.doc_type, body=body)['count']
        # 如果公众号对应的index不存在则发生错误 也就说明该文章并未被创建索引
        except Exception as e:
            result = 0
        return result

if __name__ == '__main__':
    index = IndexDoc.get_all_indices()
    print(index)

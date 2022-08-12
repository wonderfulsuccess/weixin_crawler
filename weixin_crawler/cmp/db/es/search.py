"""
作为搜索模块 应该提供哪些功能
执行一次搜索创建一个对象
"""
import re
from cmp.db.es.config import search_template
from copy import deepcopy
from cmp.db.es import es_instance
from utils.base import logger, debug_p


class Search():
    def __init__(self, search_data, index_list, from_size={"from":0,"size":10}, fields=['title', 'article', 'author', 'digest', 'comments'], doc_type='gzh_article', source=None):
        """
        :param index_list: 所需要搜搜的索引列表
        :param search_words: 搜索关键字 支持通配符
        """
        self.index_list = index_list
        self.search_data = search_data
        self.doc_type = doc_type
        self.fileds = fields
        self.from_size=from_size
        self.source = source

    def search(self):
        """
        :return: 执行搜索动作
        """
        # 根据公众号的昵称
        indices = []
        st = deepcopy(search_template)
        dls = self.search_data_preprocess()
        st.update(dls)
        if self.source != None:
            st["_source"] = self.source
        # 添加搜索字段
        # st['_source'] = self.fileds
        # 更新from 和 size 支持分页
        try:
            st["from"] = self.from_size["from"]
            st["size"] = self.from_size["size"]
        except:
            logger.warning("from_size字段错误 %s"%(str(self.from_size)))
        # 指定 搜索的索引范围
        if not self.index_list:
            indices = '*'
        else:
            indices = self.index_list
        try:
            result = es_instance.search(index=indices, body=st)['hits']
            # result = es_instance.search(index=indices, doc_type=self.doc_type, body=st)['hits']
            return result
        except Exception as e:
            print(e)
            logger.error("搜索错误 可能是有指定了不存在的搜索范围没有建立索引%s"%(str(indices)))
            return False

    def search_data_preprocess(self):
        """
        :return: 预处理搜索关键字 分理出其中的搜索模式
        :param search_data:
        :return: 对即将搜索的数据进行预处理 解析搜索模式
        数据中包含模式：
        双引号包含的内容使用match_phrase全匹配,双引号之外的内容使用分词模式match
        排序模式 指定排序字段以及升降方式
        举例："必须包含词"分词模式-time-1
        根据搜索数据中指定的规则返回查询的query、sort等字段数据
        """
        # 由于每种文章的index都不一样 该字典应该由 具体的应用提供
        sort_mapping = {
            "loc":"mov",            #文章发布位置
            "author":"author",      #作者
            "time":"p_date",        #发文时间
            # "read":"read_num",      #阅读量
            # "like":"like",          #点赞量
            "comm":"comments",      #评论量
            "reward":"reward_num",  #赞赏量
            "unk":"_score",         #未知 就按照默认的分数排序
        }
        sort_dir_mapping = {
            '0':"asc",
            '1':"desc",
        }
        # 带有查询规则 分离搜索数据 排序字段和排序顺序
        if len(re.findall('-',self.search_data))==2:
            part_data = self.search_data.split('-')
            try:
                sort_dir = sort_dir_mapping[part_data[-1]]
                sort_field = sort_mapping[part_data[-2]]
            except:
                sort_dir = sort_dir_mapping['1']
                sort_field = sort_mapping['unk']
        # 普通查询
        else:
            sort_dir = sort_dir_mapping['1']
            sort_field = sort_mapping['unk']
        search_data = self.search_data.split('-')[0]
        # 找出必须完整包含的字段
        data_match_phrase = [x.replace('"','') for x in re.findall(r'"\S*?"', search_data)]
        data_match = search_data.replace('"','')
        # 创建必须完整包含字段的Elsticsearch搜索描述数据
        for x in data_match_phrase:
            data_match = data_match.replace(x,'').replace(' ','')
        query_value = {
            "bool": {
                "should": []
            }
        }
        match_phrase_item = {
            "match_phrase": {}
        }
        match_item = {
            "match": {}
        }
        # 创建分词字段 英文不分词根据空格
        for f in self.fileds:
            if data_match != '':
                should_item = deepcopy(match_item)
                should_item["match"][f] = data_match
                query_value["bool"]["should"].append(should_item)

            for item in data_match_phrase:
                should_item = deepcopy(match_phrase_item)
                should_item["match_phrase"][f]=item
                query_value["bool"]["should"].append(should_item)

        sort_value = [
            {
                sort_field: {
                    "order": sort_dir
                }
            }
        ]
        return {"query":query_value,"sort":sort_value}


if __name__ == '__main__':
    from utils.base import debug_p
    s = Search('教育', ['gzh_阿拉升学说'], 'gzh_article')
    data = s.search()
    debug_p(data)

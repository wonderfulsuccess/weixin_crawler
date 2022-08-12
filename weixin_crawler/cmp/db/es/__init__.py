"""
搜索的两个关键步骤 建立索引 和 执行搜索
"""
from elasticsearch import Elasticsearch
es_instance = Elasticsearch(sniffer_timeout = 120)

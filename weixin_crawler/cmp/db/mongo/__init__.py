# mongodb
from pymongo import MongoClient
from config import MONGODB_PORT, MONGODB_HOST, MONGODB_NAME
db_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db_instance = db_client[MONGODB_NAME]


class CollectionOperation():
    """
    mongodb
    """
    def __init__(self, table):
        """
        :param table: 实际上table在mongodb中被称为 collection 为了名称统一此处仍成为table
        table 的数据结果见data_scheme
        """
        self.table = db_instance[table]

    def count(self, **kwargs):
        """
        :return:返回符合条件数据的总数
        """
        return self.table.count_documents(kwargs)

    def delete(self, **kwargs):
        """
        :param kwargs: 用字典表示的过滤器
        :return: 根据match中提供的符合信息删除文章 支持全部删除
        """
        self.table.delete_many(kwargs)

    def get(self, **kwargs):
        """
        :param kwargs:
        :return: 返回符要求的数据生成器
        
        """
        data = self.table.find(kwargs)
        return data

    def insert(self, key, data, check_exist=True):
        """
        :param data: []多个数据，或单个数据{}
        :param key: 更新模式下判重的依据
        :param check_exist:是否需要检查存在(更新模式)
        :return: 插入一条数据或多个数据 在进行数据写入 基本上只需使用这一个API
        """
        res = 'INSERT'
        # 需要检查更新
        if check_exist:
            # 单个数据
            if type(data) == dict:
                res = self._update_one(key, data)
            # 多个数据
            elif type(data) == list:
                res = self._update_many(key, data)
        # 不用检查更新 速度会快一些
        else:
            # 单个数据
            if type(data) == dict:
                self._insert_one(data)
            # 多个数据
            elif type(data) == list:
                self._insert_many(data)
        return res

    def _insert_one(self, data):
        """
        :param data: {}
        :return: 插入一条数据
        """
        return self.table.insert_one(data).inserted_id

    def _insert_many(self, data):
        """
        :param data: []
        :return: 插入多条数据
        """
        self.table.insert_many(data)
        return len(data)

    def _update_one(self, key, data):
        """
        :param key: 判存字段
        :param data: {}
        :return: 更新或插入一条数据 用data中的字段更新key作为判断是否存在 存在更新 不存在就插入
        """
        result = self.table.find_one({key: data[key]})
        # 数据存在可以更新
        if type(result) is dict:
            self.table.update_one({key: data[key]}, {"$set": data})
            op_result = 'UPDATE'
        # 数据不存在调用插入
        else:
            self._insert_one(data)
            op_result = 'INSERT'
        return op_result

    def _update_many(self, key, data):
        """
        :param key: 判存字段
        :param data: []
        :return: 更新或插入多个数据 只要有一个数据是更新模式 返回UPDATE否则返回INSERT
        """
        res = 'INSERT'
        for d in data:
            if self._update_one(key, d) == 'UPDATE':
                res = 'UPDATE'
        return res

    def custom(self):
        """
        :return: 返回table 方便用户自定义操作
        """
        return self.table


if __name__ == "__main__":
    data = {'video_num': 0, 'pic_num': 8, 'comment_id': '643962374688604160', 'id': '6b6934a83fa4385ed4ec53f987e07b5f'}
    col = CollectionOperation('爱迪斯')
    col.insert('id', data)

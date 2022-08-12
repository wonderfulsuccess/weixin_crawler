from cmp.db.sqlite.data_schema import sqlite_db
from utils.base import logger


class CollectionOperation():
    """
    提供sqllite的API
    使用时传入一个data_schema中的类即可
    正确的做法应该是使用sql语句操作 以后再来更新 接口
    详细文档见 http://docs.peewee-orm.com/en/latest/peewee/query_operators.html
    """
    def __init__(self, table):
        self.table = table

    def count(self, key=None,value=None, _type=1):
        """
        :param key: 来自Data中的某个属性
        :param value: 希望匹配概述性的值
        :param _type: 1:包含模式 2:相等模式
        :return:返回符合条件数据的总数
        """
        if _type == 1:
            return self.table.select().where(getattr(self.table,key).contains(value)).count()
        elif _type == 2:
            return self.table.select().where(getattr(self.table,key)==value).count()

    def delete(self, key=None, value=None, _type=1):
        """
        :param key:
        :param value:
        :return: 删除符合条件的数据
        """
        # 删除包含指定字符的数据
        if key:
            if _type == 1:
                query = self.table.delete().where(getattr(self.table,key).contains(value))
            elif _type == 2:
                query = self.table.delete().where(getattr(self.table,key)==value)
        # 全部删除
        else:
            query = self.table.delete()
        return query.execute()

    def get(self, key=None, value=None, _type=1):
        """
        :param key:
        :param value:
        :param _type: 1:包含模式 2:相等模式
        :return: 返回符合查询结果的数据
        """
        if key:
            # 包含模式
            if _type == 1:
                return self.table.select().where(getattr(self.table,key).contains(value))
            # 相等模式
            elif _type == 2:
                return self.table.select().where(getattr(self.table,key)==value)
        else:
            return self.table.select()


    def insert(self, data):
        """
        :param data:list或dict
        :return: 不存在插入 存在更新 同时支持单个数据和多个数据
        单个数据使用dict表示 多个数据使用list表示
        """
        # 插入单个数据
        res = None
        # 处理单个数据
        if type(data) is type({}):
            # 根据id判断数据是否存在
            exist = self.count('id',data['id'],_type=2)
            # 数据不存在 插入
            if exist == 0:
                self.table.create(**data)
                res = "INSERT"
            #  数据存在 更新
            else:
                self.update('id',data['id'],data)
                res = "UPDATE"
            return res
        # 处理多个数据
        elif type(data) is type([]):
            with sqlite_db.atomic():
                for d in data:
                    # 根据id判断数据是否存在
                    exist = self.count('id',d['id'],_type=2)
                    # 数据不存在 插入
                    if exist == 0:
                        self.table.create(**d)
                        res = "INSERT"
                    # 数据存在 更新
                    else:
                        self.update('id',d['id'],d)
                        res = "UPDATE"
            return res

        else:
            logger.error("待插入的数据有误%s"%(str(data)))
            return "ERROR"

    def update(self, key, value, data):
        """
        :param key:
        :param value:
        :param data:
        :return: 更新一条数据
        """
        query = self.table.update(**data).where(getattr(self.table,key)==value)
        return query.execute()

    def custom(self):
        """
        :return: 返回table 方便用户自定义操作
        """
        return self.table


if __name__ == "__main__":
    pass

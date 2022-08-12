"""
提供数据设置API
"""
from cmp.db.mongo import CollectionOperation
col_settings = CollectionOperation('settings')


class Settings():
    def __int__(self):
        pass

    def get(self):
        """
        :return: 获取所有的设置字段{}
        """
        sd = col_settings.get()
        settings_data = {}
        for s in sd:
            settings_data[s['key']] = s['value']
        # 注入代理ip地址
        from utils.network import get_ip
        settings_data['proxy_server'] = get_ip()
        return settings_data

    def insert(self, settings_data_dict):
        """
        :param settings_data_dict: settings数据本质上是一个字典
        :return: 插入或修改
        """
        # 将dict转化为list 例如 {'name':'Frank Wang', 'age':18} -> [{'key':'name', 'value':'Frank Wang'},{'key':'age', 'value':18}]
        settings_data_list = []
        for key in settings_data_dict:
            item = {}
            item['key'] = key
            item['value'] = settings_data_dict[key]
            settings_data_list.append(item)
        col_settings.insert('key', settings_data_list)

    def delete(self, key, all=False):
        """
        :param key:准确的key
        :param all:
        :return:
        """
        if all:
            col_settings.delete()
        else:
            col_settings.delete(key=key)

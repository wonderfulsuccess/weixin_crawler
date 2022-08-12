"""
请求参数可能存放在redis、sqlite等多种数据存储介质中
模块提供参数查询和删除的功能 使用不同的存储介质 修改该模块即可
"""
from instance import col_req_data


class SQLite():
    """
    请求参数存放在sqlite中
    """
    @classmethod
    def get(cls):
        """
        :return: 返回全部参数
        """
        all_raw_req_data = []
        res = col_req_data.get()
        for r in res:
            all_raw_req_data.append({'key':r.key, 'time':r.time, 'value':r.value})
        return all_raw_req_data

    @classmethod
    def delete(cls, _key=None, _type=1):
        """
        :param _type: 1包含或2者相等
        :param _key: key或者key的一部分
        :return: 删除包含key或者等于key的全部参数
        """
        # 删除指定的参数
        if _key:
            col_req_data.delete(key='key', value=_key, _type=_type)
        # 删除全部参数
        else:
            col_req_data.delete()


class File():
    """
    请求参数存在文件中
    """
    pass


class Redis():
    """
    请求参数存放在redis中
    """
    pass


class Mongodb():
    """
    请求参数存放在mongodb中
    """
    pass



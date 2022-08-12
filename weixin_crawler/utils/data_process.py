# 字符串到字典
def str_to_dict(s, join_symbol="\n", split_symbol=":"):
    """
    字符串到字典 支持自定义键值间隔符和成员间隔符
    :param s: 原字符串
    :param join_symbol: 连接符
    :param split_symbol: 分隔符
    :return: 字典
    """
    s_list = s.split(join_symbol)
    data = dict()
    for item in s_list:
        item = item.strip()
        if item:
            k, v = item.split(split_symbol, 1)
            data[k] = v.strip()
    return data


# 字典到字符串
def dict_to_str(data, join_symbol="&", split_symbol="="):
    """
    :param data:dict数据
    :param join_symbol:不同成员之间的连接符
    :param split_symbol:名称和值分隔符
    :return: 字典转换为字符串
    """
    s = ''
    for k in data:
        s += str(k)+split_symbol+str(data[k])+join_symbol
    return s[:-1]


def update_dict_by_dict(whole_dict, part_dict, keys=None):
    """
    :param whole_dict:
    :param part_dict:
    :param keys:
    :return:根据指定的keys 用part_dict的value更新whole_dict的value
    """
    if keys == None:
        whole_dict.update(part_dict)
        return whole_dict
    else:
        for key in keys:
            if key in part_dict:
                whole_dict[key] = part_dict[key]
        return whole_dict

# 生成唯一的hash值
import hashlib
def get_md5(data):
    """
    由于hash不处理unicode编码的字符串（python3默认字符串是unicode）
        所以这里判断是否字符串，如果是则进行转码
        初始化md5、将url进行加密、然后返回加密字串
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    md = hashlib.md5()
    md.update(data)
    return md.hexdigest()

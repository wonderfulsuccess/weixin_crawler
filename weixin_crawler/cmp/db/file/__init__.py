import codecs
import os
from utils.base import logger


def save(key, value, path='./'):
    """
    :param key:
    :param value:
    :return: 将键值对保存为文件 文件路径不存在会自动创建
    """
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        with codecs.open(path+str(key),'w',encoding='utf8') as f:
            f.write(str(value))
    except:
        logger.error('文件保存失败%s'%(path+key))


class CollectionOperation():
    """
    对某个路径下的各个文件提供辅助操作, 类似一个数据库的collection
    """
    def __init__(self, dir):
        self.dir = dir
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def all(self, key=None):
        """
        :param key :是否只返回包含特定子字符串的文件名称
        :return: list形式返回路径下的所有文件
        """
        file_list = [f for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir, f))]
        if not key:
            return file_list
        else:
            return [f for f in file_list if key in f]

    def count(self,key=None):
        """
        :param key:
        :return:文件的数量
        """
        return len(self.all(key))


    def delete(self, key=None):
        """
        :param key:
        :return: 删除包含某个子字符串的文件 删除全部文件
        """
        file_list = self.all(key)
        for f in file_list:
            os.remove(self.dir+f)
        return key

    def get(self, key):
        """
        :param key:
        :return:获取一个文件文件的内容
        """
        try:
            with codecs.open(self.dir+key,'r',encoding='utf8') as f:
                text = f.read().replace("'",'"')
        except:
            text = None
            logger.error("%s文件不存在"%(self.dir+key))
        return text

    def insert(self, key, value):
        """
        :param name:
        :param value:
        :return: 保存一条一个新文件 如果文件名已经存在则更新
        """
        with codecs.open(self.dir+key,'w',encoding='utf8') as f:
            f.write(str(value))
        return key

if __name__ == "__main__":
    col = CollectionOperation('./frank/')
    col.insert('123','123123')
    print(col.all())
    print(col.get('123'))
    print(col.count())
    print(col.delete())

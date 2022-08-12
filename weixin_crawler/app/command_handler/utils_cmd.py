"""
处理一些常规命令
"""
from utils.base import logger
from utils.front import command_log


class MovStr2Int:
    """
    :return: 将所有公众号数据的mov从str转化为int
    """
    def run(self, command, cmd_args):
        from app.api.gzh import Finished
        from cmp.db.mongo import CollectionOperation
        for gzh in Finished().get()['finished']:
            col = CollectionOperation(gzh['nickname'])
            articles_buffer = []
            for a in col.get():
                if type(a['mov']) == str:
                    a['mov'] = int(a['mov'])
                    articles_buffer.append(a)
            col.insert('id', articles_buffer)
            logger.info('转化完成 %d %s'%(len(articles_buffer), gzh['nickname']))
            command_log('转化完成 %d %s'%(len(articles_buffer), gzh['nickname']))


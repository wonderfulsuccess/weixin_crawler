"""
为已经采集的公众号页面提供数据支持
"""
from instance import col_crawler_log
from cmp.db.mongo import CollectionOperation
from utils.data_process import get_md5


class Finished:
    def __init__(self):
        pass

    def get(self):
        """
        :return:获取所有公众号列表
        """
        info_data = []
        gzh_num = 0
        total_article_num = 0
        gzhs = col_crawler_log.get()
        cnt = 1
        for i in gzhs:
            gzh_num += 1
            col_data = CollectionOperation(i['nickname'])
            table_line_data = {}
            # 获取文章总数
            total_num = col_data.count()
            total_article_num += total_num
            # 获取含有阅读数据的文章总数
            article_num = col_data.count(read_num={'$gt': -2})
            # 生成一行表格的数据
            table_line_data['id'] = cnt
            table_line_data['nickname'] = i['nickname']
            table_line_data['total_articles'] = total_num
            table_line_data['reading_data_articles'] = article_num
            table_line_data['time'] = i['time'].timestamp()
            cnt += 1
            info_data.append(table_line_data)
        return {'finished': info_data, 'stat_data': {'gzh_num':gzh_num, 'article_num': total_article_num}}

    def get_article_list(self, page_info, **kwargs):
        """
        :param page_info: {'nickname','start','end'}
        :return: 返回一个公众号的全部文章列表
        """
        from pymongo import DESCENDING
        col_data = CollectionOperation(page_info['nickname'])
        info_data = []
        cnt = 1
        # 返回文章切片 按时间逆向排序 越靠近现在越靠前
        articles = col_data.table.find(kwargs).sort("p_date", DESCENDING)[int(page_info['start']):int(page_info['end'])]
        for a in articles:
            item = {}
            item['id'] = cnt
            item['mov'] = str(a['mov'])

            if 'read_num' in a:
                item['read'] = a['read_num']
            else:
                item['read'] = '-'

            if 'like_num' in a:
                item['like'] = a['like_num']
            else:
                item['like'] = '-'

            if 'reward_num' in a:
                item['reward'] = a['reward_num']
            else:
                item['reward'] = '-'

            if 'comment_num' in a:
                item['comment'] = a['comment_num']
            else:
                item['comment'] = '-'

            item['like_folder'] = 0
            if ('like_folder' in a) and (a['like_folder']):
                item['like_folder'] = 1

            item['date'] = a['p_date'].timestamp()
            item['title'] = a['title']
            item['url'] = a['content_url']
            item['md5'] = get_md5(a['content_url'])
            cnt += 1
            info_data.append(item)
        return info_data

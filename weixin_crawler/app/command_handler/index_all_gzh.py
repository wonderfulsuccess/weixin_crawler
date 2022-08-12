"""
run 方法必须
"""
from utils.front import command_log
class IndexAllGZH():
    def __int__(self):
        pass

    def run(self, command, cmd_args):
        import time
        begin_time = time.time()
        print(command, cmd_args)
        from instance import col_crawler_log
        gzhs = col_crawler_log.get()
        clean_gzhs = []
        for g in gzhs:
            clean_gzhs.append(g['nickname'])

        # 使用用自己定义的公众号列表建立索引
        if len(cmd_args):
            if set(cmd_args) <= set(clean_gzhs):
                clean_gzhs = cmd_args

        for nickname in clean_gzhs:
            command_log('> 搜集文章正文 %s'%(nickname))
            # 强制重新请求文章的html数据
            from app.weixin_crawler.article import get_all_article_by_nickname
            get_all_article_by_nickname(nickname, worker_num=128)

            # 根据公众号的昵称从数据库中读取数据让后在es中建立索引
            command_log('>> 创建索引 服务搜索 %s'%(nickname))
            from app.api.crawler import index_gzh
            index_gzh(nickname)
            command_log('>>> 完成 %s'%(nickname))
        command_log('指令完成 用时%.1f分钟'%((time.time()-begin_time)/60))


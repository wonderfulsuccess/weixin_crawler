"""
页面路由
"""
from web_server import web_app
from flask import render_template, send_from_directory
from instance import PLATFORM


@web_app.route('/', methods=['GET'])
def index():
    """
    :return: 返回首页
    """
    return render_template('index.html')


@web_app.route('/img/<filename>', methods=['GET'])
def get_img(filename):
    """
    :param filename:
    :return: 返回一个静动态文件
    """
    print(filename)
    return send_from_directory(directory=r'web_server/static/img/',filename=filename)


# 返回文章的html
@web_app.route('/html/<nickname>/<md5>', methods=['GET'])
def get_html_doc(nickname, md5):
    """
    :param filename:
    :return: 返回一个静动态文件
    """
    from cmp.db.mongo import CollectionOperation
    if CollectionOperation(nickname).count(id=md5, comment_id={'$exists': True}):
        from webbrowser import open
        import os
        if PLATFORM == 'win':
            file_name = os.getcwd() + r'\\web_server\\static\\html\\'+nickname+'\\'+ md5 + '.html'
            if os.path.isfile(file_name):
                open(file_name)
            else:
                return '找不到该文章 可能是没有迁移到新版本的WCplus 请先从旧版本的WCplus中复制或移动到新版本的WCplus的web_server/static/html目录下'
        else:
            file_name = os.getcwd() + r'/web_server/static/html/'+nickname+'/'+ md5 + '.html'
            if os.path.isfile(file_name):
                open('file://' + file_name)
            else:
                return '找不到该文章 可能是没有迁移到新版本的WCplus 请先从旧版本的WCplus中复制或移动到新版本的WCplus的web_server/static/html目录下'

        return ('', 204)
    else:
        return '未保存该文章 请先采集'

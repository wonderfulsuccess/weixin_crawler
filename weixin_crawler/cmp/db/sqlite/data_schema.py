# sqlite
from peewee import SqliteDatabase
from config import SQLITE_DB_NAME
sqlite_db = SqliteDatabase(SQLITE_DB_NAME)
sqlite_db.connect()

from peewee import Model
from peewee import CharField,IntegerField,TextField,DateTimeField
from datetime import datetime
"""
创建数据格式
"""

# 微信公众号文章结构
class Data(Model):
    # 定义新的应用时该结构需要重写 但是必须包含id字段
    id                = CharField(default="")       # 唯一id
    nickname          = CharField(default="")       #公众号昵称 string
    title             = CharField(default="")       #文章标题 string
    article_id        = IntegerField(default=-2)    #一个公众号的文章id int
    content_url       = CharField(default="")       #文章真实url url
    source_url        = CharField(default="")       #文章原文url url
    digest            = TextField(default="")       #人工摘要 string
    machine_digest    = TextField(default="")       #自动摘要 string
    cover             = CharField(default="")       #封面url url
    p_date            = DateTimeField(default= datetime(2000,1,1))#发布时间 datetime
    with_ad           = IntegerField(default=-2)    #有无广告 bool
    pic_num           = IntegerField(default=-2)    #插图数 int
    video_num         = IntegerField(default=-2)    #视频数量 int
    read_num          = IntegerField(default=-2)    #阅读量 int
    like_num          = IntegerField(default=-2)    #点赞量 int
    comment_id        = CharField(default="")       #评论id string
    comment_num       = IntegerField(default=-2)    #评论数量 int
    comments          = TextField(default="{}")     #精选评论内容 dict
    reward_num        = IntegerField(default=-2)    #赞赏数量 int
    author            = CharField(default="")       #作者 string
    copyright_stat    = CharField(default="")       #是否原创
    mov               = IntegerField(default=-2)    #主副 int
    title_emotion     = IntegerField(default=-2)    #标题情感 int
    title_token       = TextField(default="[]")     #标题分词 list
    title_token_len   = IntegerField(default=-2)    #分词长度 int
    human_digest_token= TextField(default="[]")     #人工摘要分词 list
    article           = TextField(default="")       #文本内容 markdown
    html              = TextField(default="")       #文章原始html
    article_token     = TextField(default="[]")     #正文分词 list
    article_token_len = IntegerField(default=-2)    #正文分词长度 int
    c_date            = DateTimeField(default= datetime(2000,1,1))#爬取时间
    class Meta:
        database = sqlite_db

class ReqData(Model):
    # 定义新的应用时该结构需要重写 但是必须包含id字段
    id                = CharField(default="")       # 唯一id 通key
    time              = DateTimeField(default= datetime.now()) # 更新时间
    key               = CharField(default="")       # 请求参数的键
    value             = TextField(default="")       # 请求参数的值
    class Meta:
        database = sqlite_db

class CrawlerLog(Model):
    # 记录公众号更新的时间和文章数量
    id                = CharField(default="")       # 唯一id nickname
    nickname          = CharField(default="")       # 公众号昵称
    num               = TextField(default="")       # 更新数量
    time              = DateTimeField(default= datetime.now()) # 更新时间
    class Meta:
        database = sqlite_db

sqlite_db.create_tables([Data,ReqData,CrawlerLog])

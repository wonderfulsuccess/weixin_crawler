from datetime import datetime


# 微信公众号文章结构
article_scheme = {
    # 定义新的应用时该结构需要重写 但是必须包含id字段
    'id'                : "",                    # 唯一id 使用url的md5
    'nickname'          : "",                    #公众号昵称 string
    'title'             : "",                    #文章标题 string
    'article_id'        : -2,                    #一个公众号的文章id int
    'content_url'       : "",                    #文章真实url url
    'source_url'        : "",                    #文章原文url url
    'digest'            : "",                    #人工摘要 string
    'machine_digest'    : "",                    #自动摘要 string
    'cover'             : "",                    #封面url url
    'p_date'            : datetime(2000, 1, 1),    #发布时间 datetime
    'with_ad'           : -2,                    #有无广告 bool
    'pic_num'           : -2,                    #插图数 int
    'video_num'         : -2,                    #视频数量 int
    'read_num'          : -2,                    #阅读量 int
    'like_num'          : -2,                    #点赞量 int
    'comment_id'        : "",                    #评论id string
    'comment_num'       : -2,                    #评论数量 int
    'comments'          : {},                    #精选评论内容 dict
    'reward_num'        : -2,                    #赞赏数量 int
    'author'            : "",                    #作者 string
    'copyright_stat'    : "",                    #是否原创
    'mov'               : -2,                    #主副 int
    'title_emotion'     : -2,                    #标题情感 int
    'title_token'       : [],                    #标题分词 list
    'title_token_len'   : -2,                    #分词长度 int
    'human_digest_token': [],                    #人工摘要分词 list
    'article'           : "",                    #文本内容 markdown
    'html'              : "",                    #文章原始html
    'article_token'     : [],                    #正文分词 list
    'article_token_len' : -2,                    #正文分词长度 int
    'c_date'            : datetime(2000, 1, 1),    #爬取时间
}

req_data_scheme = {
    # 定义新的应用时该结构需要重写 但是必须包含id字段
    'id'                : "",                   # 唯一id 通key
    'time'              : datetime.now(),       # 更新时间
    'key'               : "",                   # 请求参数的键
    'value'             : "",                   # 请求参数的值
}

crawler_log_scheme = {
    # 记录公众号更新的时间和文章数量
    'id'                : "",                   # 唯一id nickname
    'nickname'          : "",                   # 公众号昵称
    'num'               : "",                   # 更新数量
    'time'              : datetime.now()        # 更新时间
}

def fill_by_scheme(scheme, data, with_default=False):
    """
    :param scheme: 含有一条article部分或者全部的数据
    :param data: 子key数据
    :param with_default: 是否需要scheme中的默认值
    :return:根据article_scheme中指定的字段提取article_seg中的数据 这样可以保证数据库中没有无关字段
    """
    article = {}
    for key in scheme:
        if key in data:
            article[key] = data[key]
        else:
            if with_default:
                article[key] = scheme[key]
    return article

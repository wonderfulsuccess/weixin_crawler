# 选择需要建立索引的字段 尽量保证字段的名称和mongodb一致 认为为这些字段建立索引提供搜索比较有实际意义
#
doc_schema = {
    # "nickname":     {"type":"text","analyzer": "ik_max_word","search_analyzer": "ik_max_word"},
    "title":        {"type":"text","analyzer": "ik_max_word","search_analyzer": "ik_max_word"},
    # "article_id":   {"type":"integer"},
    # 对于页面文章 统一使用文章的url作为id
    "id":  {"type":"text"},
    # "source_url":   {"type":"text"},
    "digest":       {"type":"text","analyzer": "ik_max_word","search_analyzer": "ik_max_word"},
    # "cover":        {"type":"text"},
    "p_date":       {"type":"date"},
    # "with_ad":      {"type":"boolean"},
    "pic_num":      {"type":"integer"},
    "video_num":    {"type":"integer"},
    "read_num":     {"type":"integer"},
    "like_num":     {"type":"integer"},
    # "comment_id":   {"type":"text"},
    "comment_num":  {"type":"integer"},
    "comments":     {"type":"text","analyzer": "ik_max_word","search_analyzer": "ik_max_word"},
    "reward_num":   {"type":"integer"},
    "author":       {"type":"text","analyzer": "ik_max_word","search_analyzer": "ik_max_word"},
    "mov":          {"type":"short"},
    # "title_emotion":{"type":"text","analyzer": "ik_max_word","search_analyzer": "ik_max_word"},
    # "title_token":  {"type":"nested"},
    # "title_token_len":{"type":"integer"},
    # "human_digest_token":{"type":"nested"},
    "article":      {"type":"text","analyzer": "ik_max_word","search_analyzer": "ik_max_word"},
    # "article_token":{"type":"nested"},
    # "article_token_len":{"type":"integer"},
    # "c_date":       {"type":"date"}
}

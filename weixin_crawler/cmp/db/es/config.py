

# 搜索body模板
search_template = {
    "query":{"match_all":{}},
    "from":0,
    "size":20,
    "sort":[],
    "highlight" : {
        "pre_tags" : ["<span style='color:#dd4b39'>"],
        "post_tags" : ["</span>"],
        "fields" : {
            "title":{},
            "digest":{},
            "author":{},
            "comments":{},
            "article":{}
        }
    }
}

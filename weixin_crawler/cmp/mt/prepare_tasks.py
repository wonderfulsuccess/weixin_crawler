def prepare_tasks():
    """
    :return: 产生任务列表
    """
    for t in range(100):
        yield {'index':t, 'id':t}

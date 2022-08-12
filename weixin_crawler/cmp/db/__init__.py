def db_select(des):
    """"
    :param des:
    :return: 根据数据保存目的返回正确的CollectionOperation
    """
    if des == 'FILE':
        from cmp.db.file import CollectionOperation
        return CollectionOperation
    elif des == 'SQLITE':
        from cmp.db.sqlite import CollectionOperation
        return CollectionOperation

    # elif des == 'MONGO':
    #     from db.sqlite import CollectionOperation
    #     return CollectionOperation
    #
    # elif des == 'REDIS':
    #     from db.sqlite import CollectionOperation
    #     return CollectionOperation
    #
    # elif des == 'ES':
    #     from db.sqlite import CollectionOperation
    #     return CollectionOperation

    else:
        return None

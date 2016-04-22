from utils.mongodb_handler import MongoDB


def get_mongodb():
    return MongoDB().get_database()


def news_verify(news):
    params = news.keys()
    # if '' not in params:
    #     return False
    return True
from datetime import datetime
from time import strftime, localtime

from utils.mongodb_handler import MongoDB


def get_mongodb():
    return MongoDB().get_database()


def news_verify(news):
    params = news.keys()
    # if '' not in params:
    #     return False
    return True

def str_from_timestamp(timestap):
    time_format = "%Y-%m-%d %H:%M:%S"
    return strftime(time_format, localtime(timestap))
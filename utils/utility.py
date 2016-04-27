# coding=utf-8
from datetime import datetime
from time import strftime, localtime
import re

from extractor import GeneralExtractor
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


def clean_date_time(string):
    """清洗时间

    :param string: 包含要清洗时间的字符串
    :type string: str
    :return: 生成的字符串, 格式为 2016-02-01 12:01:59
    :rtype: str
    """
    date_time_string = ""
    p_date_list = [
        r"((20\d{2})[/.-])?(\d{2})[/.-](\d{2})",
        r"((20\d{2})?年)?(\d{2})月(\d{2})",
        u"((20\d{2})?\u5e74)?(\d{2})\u6708(\d{2})",

        r"((20\d{2})[/.-])?(\d{1})[/.-](\d{2})",
        r"((20\d{2})?年)?(\d{1})月(\d{2})",
        u"((20\d{2})?\u5e74)?(\d{1})\u6708(\d{2})",

        r"((20\d{2})[/.-])?(\d{2})[/.-](\d{1})",
        r"((20\d{2})?年)?(\d{2})月(\d{1})",
        u"((20\d{2})?\u5e74)?(\d{2})\u6708(\d{1})",

        r"((20\d{2})[/.-])?(\d{1})[/.-](\d{1})",
        r"((20\d{2})?年)?(\d{1})月(\d{1})",
        u"((20\d{2})?\u5e74)?(\d{1})\u6708(\d{1})",
    ]
    for p_date in p_date_list:
        date_match = re.search(p_date, string)
        if date_match is not None:
            break
    else:
        return date_time_string
    p_time = r"(\d{2}):(\d{2})(:(\d{2}))?"
    time_match = re.search(p_time, string)
    now = datetime.now()
    year_now = now.strftime("%Y")
    hour_now = now.strftime("%H")
    minute_now = now.strftime("%M")
    second_now = now.strftime("%S")
    if date_match is None:
        return date_time_string
    else:
        date_groups = date_match.groups()
    if time_match is None:
        time_groups = (hour_now, minute_now, ":" + second_now, second_now)
    else:
        time_groups = time_match.groups()
    year = date_groups[1]
    month = date_groups[2]
    if len(month) == 1:
        month = "0" + month
    day = date_groups[3]
    if len(day) == 1:
        day = "0" + day
    hour = time_groups[0]
    minute = time_groups[1]
    second = time_groups[3]
    if year is None:
        year = year_now
    if second is None:
        second = second_now
    date_string = "-".join([year, month, day])
    time_string = ":".join([hour, minute, second])
    date_time_string = date_string + " " + time_string
    return date_time_string


def extractor(content_html):
    string = r'<div>' + content_html + r'</div>'
    ex = GeneralExtractor(string)
    content = ex()[4]
    return content
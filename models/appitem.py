# -*- coding: utf-8 -*-
import time
import uuid

from utils.utility import str_from_timestamp


class AppItem(object):
    title = None  # 标题 str
    publish_time = None  # 发布时间 str
    content = None  # 内容 ['img': '', 'text': '', 'video': '',...]
    app_name = None # 抓取源APP的名称
    app_icon = None # 抓取源APP的icon
    status = 1 # 状态标识 1:正常;2:时间大于当前+24H
    author = None
    content_html = None  # 文章原始内容

    insert_time = None
    summary = None  # 摘要 str
    love = None  # 喜爱 int
    up = None  # 顶 int
    down = None  # 踩 int

    docid = None  # 网站内部唯一标识
    channel = None  # 频道 str
    crawl_url = None  # 抓取网址 str
    # image_list = None    # 新闻 meta 图片列表， 只为向下兼容

    key = None  # redis key, base64 for crawl_url
    start_url = None  # start url, record to get channel info in pipeline

    start_meta_info = None  # meta info from start request dict or None

    comment_url = None  # comment url for comment spider
    comment_queue = None  # comment redis queue for comment spider

    @staticmethod
    def get_table_name():
        return 'news'

    def get_item_from_request_param(self, param_dict):
        self.title = param_dict['article_title']
        self.app_name = param_dict['app_name']
        self.app_icon = param_dict['app_icon']
        self.content_html = param_dict['detail_html']
        self.docid = uuid.uuid1().hex
        if 'author' in param_dict and param_dict['author']:
            self.author = param_dict['author']
        if 'summary' in param_dict and param_dict['summary']:
            self.summary = param_dict['summary']
        self.publish_time = str_from_timestamp(int(param_dict['published_date']))
        if int(param_dict['published_date'])/1000 > time.time() + 24*60*60:
            self.status = 2
        self.content_html = param_dict['detail_html']
        self.insert_time =str_from_timestamp(time.time())
        return self



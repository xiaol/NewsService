# -*- coding: utf-8 -*-

from models import Models


class AppItem(object):
    title = None  # 标题 str
    tags = None  # 关键字 ['str',...]
    summary = None  # 摘要 str
    publish_time = None  # 发布时间 str
    content = None  # 内容 ['img': '', 'text': '', 'video': '',...]
    province = None  # 省 str
    city = None  # 市 str
    district = None  # 区/县 str
    love = None  # 喜爱 int
    up = None  # 顶 int
    down = None  # 踩 int
    image_number = None  # 图片数 int

    docid = None  # 网站内部唯一标识
    channel = None  # 频道 str
    category = None  # 分类 str
    crawl_url = None  # 抓取网址 str
    original_url = None  # 源网址 str
    crawl_source = None  # 抓取地址 str
    original_source = None  # 源地址 str
    content_html = None  # 文章原始内容
    # image_list = None    # 新闻 meta 图片列表， 只为向下兼容

    key = None  # redis key, base64 for crawl_url
    start_url = None  # start url, record to get channel info in pipeline

    start_meta_info = None  # meta info from start request dict or None

    comment_url = None  # comment url for comment spider
    comment_queue = None  # comment redis queue for comment spider

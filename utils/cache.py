# coding: utf-8

""" 缓存相关, 目前使用的 redis """

from redis import from_url
from settings import REDIS_URL

__author__ = "Sven Lee"
__copyright__ = "Copyright 2016-2019, ShangHai Lie Ying"
__credits__ = ["Sven Lee"]
__license__ = "Private"
__version__ = "1.0.0"
__email__ = "lee1300394324@gmail.com"
__date__ = "2016-07-27 14:15"


redis = from_url(REDIS_URL, max_connections=30)

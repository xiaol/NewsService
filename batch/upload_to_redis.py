# coding=utf-8
import base64
import time
import json
import logging
import sys, os

import requests
from bs4 import BeautifulSoup
from redis import Redis
from redis import from_url

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.postgredb_handler import get_source_name, add_spider_source
from utils.utility import get_mongodb, extractor, change_text_txt
from settings import Debug, REDIS_URL, NEWS_STORE_API

_logger = logging.getLogger(__name__)


def get_redis_item_from_mongo_item(i):
    item = dict()
    item['url'] = i['key']
    item['title'] = i['title']
    item['pub_time'] = i['publish_time']
    item['docid'] = item['url']
    soup = BeautifulSoup(item['content_html'])
    video = soup.find_all('video')
    if video:
        db = get_mongodb()
        db.news.update(i, {'$set': {'task_status': 2, 'status': 4}})
        return None

    item['content'] = json.dumps(change_text_txt(extractor(i['content_html'])))
    item['channel_id'] = 35
    item['pub_name'] = i['app_name']
    item['source_name'] = i['app_name']

    item['source_online'] = 0
    item['task_conf'] = '{}'
    return item


def store_app_news(key):
    key = base64.encodestring(key).replace('=', '')
    url = NEWS_STORE_API.format(key=key)
    ret = requests.get(url)
    if ret.status_code <= 300:
        content = json.loads(ret.content)
        if content['key'] == 'succes':
            _logger.info("store %s success" % key)
        else:
            _logger.error('store %s failed: %s' % (key, content['key']))
    else:
        _logger.error('store %s failed code: %s' % (key, ret.status_code))


if __name__ == '__main__':
    source_names = set(get_source_name())
    while True:
        db = get_mongodb()
        if Debug == True:
            r = Redis()
        else:
            r = from_url(REDIS_URL, max_connections=3)
        news = db.news.find({'task_status': 0, 'status': 1}, {'_id': 0}).limit(10)
        if not news:
            time.sleep(60)
        for i in news:
            if not i['title']:
                db.news.update(i, {'$set': {'task_status': 2}})
                continue
            if i['app_name'] not in source_names and i['app_name'] + 'APP' not in source_names:
                try:
                    source_id, source_name = add_spider_source(i['app_name'])
                    source_names[source_name] = source_id
                except Exception, e:
                    print e
                    # db.news.update(i, {'$set': {'task_status': 3, 'status': 2}})
                    continue
                    exit()

            item = get_redis_item_from_mongo_item(i)
            item['source_id'] = source_id
            if item:
                key = 'news:app:' + item['url']
                r.hmset(key, item)
            # do http request to zhiguang
            if not Debug:
                store_app_news(key)
                db.news.update(i, {'$set': {'task_status': 1}})
            print 'ok'
        break
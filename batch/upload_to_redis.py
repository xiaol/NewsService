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
from utils.utility import get_mongodb, extractor, change_text_txt, clean_content
from settings import Debug, REDIS_URL, NEWS_STORE_API, NEWS_STORE_API_V2
from newsextractor import extract

_logger = logging.getLogger(__name__)


def get_redis_item_from_mongo_item(i):
    item = dict()
    item['url'] = i['key']
    item['title'] = i['title']
    item['pub_time'] = i['publish_time']
    item['docid'] = item['url']
    item['type'] = i['type']
    soup = BeautifulSoup(i['content_html'])
    video = soup.find_all('video')
    if video:
        db = get_mongodb()
        db.news.update(i, {'$set': {'task_status': 2, 'status': 4}})
        return None
    item['content_html'] = i['content_html']
    content_list = extractor(i['content_html'])
    if not content_list:
        db = get_mongodb()
        db.news.update(i, {'$set': {'task_status': 2, 'status': 5}})
        return None
    if 'link' in i:
        content_list.append({"url": i['link']})
    img_num = 0
    for j in content_list:
        if 'img' in j:
            img_num += 1
    content_list = clean_content(content_list, img_num, i['key'])
    if not content_list:
        db = get_mongodb()
        db.news.update(i, {'$set': {'task_status': 2, 'status': 5}})
        return None
    item['content'] = json.dumps(change_text_txt(content_list))

    item['img_num'] = img_num
    item['channel_id'] = '35'
    item['pub_name'] = i['app_name']
    item['source_name'] = i['app_name']

    item['source_online'] = '1'
    item['task_conf'] = '{}'
    return item


def store_app_news(key):
    key = base64.encodestring(key).replace('=', '')
    key = key.replace('\r', '')
    key = key.replace('\n', '')
    url = NEWS_STORE_API.format(key=key)
    ret = requests.get(url, timeout=30)
    if ret.status_code <= 300:
        content = json.loads(ret.content)
        if content['key'] == 'succes':
            print "store %s success v1" % key
         #   _logger.info("store %s success" % key)
        else:
            print 'store %s failed v1: %s' % (key, ret.content)
          #  _logger.error('store %s failed: %s' % (key, content['key']))
    else:
        print 'store %s failed code v1: %s' % (key, ret.status_code)
        #_logger.error('store %s failed code: %s' % (key, ret.status_code))

    url = NEWS_STORE_API_V2.format(key=key)
    ret = requests.post(url)
    if ret.status_code <= 300:
        content = json.loads(ret.content)
        if content['code'] == 2000:
            print "store %s success v2" % key
         #   _logger.info("store %s success" % key)
        else:
            print 'store %s failed v2: %s' % (key, ret.content)
          #  _logger.error('store %s failed: %s' % (key, content['key']))
    else:
        print 'store %s failed code v2: %s' % (key, ret.status_code)
        #_logger.error('store %s failed code: %s' % (key, ret.status_code))


if __name__ == '__main__':
    source_names = get_source_name()
    print source_names
    while True:
        db = get_mongodb()
        if Debug == True:
            r = Redis()
        else:
            r = from_url(REDIS_URL, max_connections=3)
        news = db.news.find({'task_status': 0, 'status': 1}, {'_id': 0}).limit(10)
        print news.count()
        if not news.count():
            time.sleep(60)
            continue
        for i in news:
            if i['type'] == 1:
                if not i['title']:
                    db.news.update(i, {'$set': {'task_status': 2}})
                    continue
                if i['app_name'] == 'Imgur':
                    db.news.update(i, {'$set': {'task_status': 3}})
                    continue
                if i['app_name'] not in source_names and i['app_name'] + 'APP' not in source_names:
                    try:
                        source_id, source_name = add_spider_source(i['app_name'])
                        source_names[i['app_name']] = source_id
                    except Exception, e:
                        print e
                        db.news.update(i, {'$set': {'task_status': 3}})
                        continue
                else:
                    source_id = source_names.get(i['app_name'])
                    if not source_id:
                        source_id = source_names.get(i['app_name'] + 'APP')
                    if not source_id:
                        continue

                item = get_redis_item_from_mongo_item(i)
                if item:
                    item['source_id'] = str(source_id)
                    key = 'news:app:' + item['url']
                    r.hmset(key, item)
                    r.expire(key, 60*60*24*3)
                else:
                    continue
                # do http request to zhiguang
                if not Debug:
                    store_app_news(key)
                    db.news.update(i, {'$set': {'task_status': 1}})

            elif i['type'] == 2:
                if 'link' not in i or not i['link']:
                    db.news.update(i, {'$set': {'status': 0}})
                    continue
                if i['app_name'] not in source_names and i['app_name'] + 'APP' not in source_names:
                    try:
                        source_id, source_name = add_spider_source(i['app_name'])
                        source_names[i['app_name']] = source_id
                    except Exception, e:
                        print e
                        db.news.update(i, {'$set': {'task_status': 3}})
                        continue
                else:
                    source_id = source_names.get(i['app_name'])
                    if not source_id:
                        source_id = source_names.get(i['app_name'] + 'APP')
                    if not source_id:
                        continue
                try:
                    print '______step 1_______'
                    ret = extract(i['link'])
                except:
                    db.news.update(i, {'$set': {'task_status': 3}})
                    continue
                if not ret[5] or not ret[0] or not ret[1]:
                    db.news.update(i, {'$set': {'task_status': 2}})
                    continue
                item = dict()
                item['url'] = i['link']
                item['title'] = ret[0]
                item['pub_time'] = ret[1]
                item['docid'] = item['url']
                item['type'] = i['type']
                item['content_html'] = i['link']
                content_list = ret[5]

                print '_________step 2_________'
                img_num = 0
                is_video = False
                for j in content_list:
                    if 'img' in j:
                        img_num += 1
                    if 'vid' in j:
                        is_video = True
                        break

                if is_video:
                    db.news.update(i, {'$set': {'task_status':2, 'status': 4}})
                    continue
                content_list = clean_content(content_list, img_num, i['link'])
                if not content_list:
                    db.news.update(i, {'$set': {'task_status':2, 'status': 5}})
                    continue
                item['content'] = json.dumps(change_text_txt(content_list))

                item['img_num'] = img_num
                item['channel_id'] = '35'
                item['pub_name'] = i['app_name']
                item['source_name'] = i['app_name']
                item['source_online'] = '1'
                item['task_conf'] = '{}'
                key = 'news:app:' + i['key']
                item['source_id'] = str(source_id)
                #key = 'news:app:' + item['url']
                r.hmset(key, item)
                r.expire(key, 60 * 60 * 24 * 3)
                if not Debug:
                    print '______step 3__________'
                    store_app_news(key)
                    db.news.update(i, {'$set': {'task_status': 1}})
                    print '______step 4_____'
            else:
                db.news.update(i, {'$set': {'status': 0}})

import time
import json
import uuid
import hashlib

from redis import Redis

from utils.utility import get_mongodb, extractor
from models.appitem import AppItem

if __name__ == '__main__':
    while True:
        db = get_mongodb()
        r = Redis()
        news = db.news.find({'task_status': 0}, {'_id': -1}).limit(10)
        if not news:
            time.sleep(60)
        for i in news:
            # item = AppItem().get_item_from_request_param(i)
            # item.content = extractor(i)
            # new_json = json.dumps(item.__dict__)
            if not i['title']:
                db.news.update(i, {'$set': {'task_status': 2}})
                continue
            item = dict()
            item['url'] = i['key']
            item['title'] = i['title']
            item['publish_time'] = i['publish_time']
            item['docid'] = item['url']
            item['content'] = extractor(i['content_html'])
            item['channel_id'] = 35
            item['source_name'] = i['app_name']
            ###
            ### 待添加source验证方法
            ###
            item['source_id'] = 1
            item['source_online'] = 0
            item['task_conf'] = '{}'
            r.set('news:app:' + item['url'],)

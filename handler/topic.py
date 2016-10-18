# coding=utf-8
import logging
import json
import random
from bson import ObjectId

from tornado.web import RequestHandler

from operations.appitem_ops import AppItemOperation
from operations.apprequest_ops import AppRequestItemOperation
from utils.response_handler import response_fail_json, response_success_json
from utils.utility import get_mongodb, get_mongodb246, extractor, change_text_txt


class NewsDataHandler(RequestHandler):
    def post(self, *args, **kwargs):
        args = self.request.arguments
        for i in args:
            args[i] = args[i][0]
        # try:
        #     news = json.loads(data)
        # except Exception, e:
        #     response = response_fail_json(ret_message=u'json报文解析失败')
        #     self.write(response)
        #     return
        args['channel_id'] = ObjectId('57ac38feda083a1c19957b1c')
        args['online_source_sid'] = 3732
        ret, message = AppRequestItemOperation().create_app_item(args)
        if ret:
            response = response_success_json(ret_message=message)
        else:
            response = response_fail_json(ret_message=message)
            logging.warning(response)
            # logging.warning('params: ' + json.dumps(args))
        self.write(response)


class JikeNewsDataHandler(RequestHandler):
    def post(self, *args, **kwargs):
        # args = self.request.arguments
        item_list_json = self.get_argument('news_list')
        item_list = json.loads(item_list_json)
        for i in item_list:
            params = dict()
            if 'app_name' not in i or 'published_date' not in i:
                continue
            params['app_name'] = i['app_name']
            params['published_date'] = i['published_date']
            params['type'] = 2
            if 'author' in i and i['author']:
                params['author'] = i['author']
            if 'summary' in i and i['summary']:
                try:
                    params['summary'] = i['summary'].encode('utf8')
                except:
                    params['summary'] = i['summary']
                if len(params['summary']) <= 60:
                    params['article_title'] = params['summary']
            else:
                params['summary'] = ''
            params['detail_html'] = params['summary']
            # if 'pictureUrl' in i and i['pictureUrl']:
            #     for j in i['pictureUrl']:
            #         params['detail_html'] += '<img src= %s />' % str(j)
            if 'link' in i and i['link']:
                params['link'] = i['link']
            else:
                logging.warning('Drop item: no link to parse')
                continue
            params['online_source_sid'] = 3733
            params['channel_id'] = ObjectId("57ac392ada083a1c19957b1d")
            ret, message = AppRequestItemOperation().create_jike_app_item(params)
            if not ret:
                # logging.warning('params: ' + json.dumps(i))
                logging.warning('Warning message: ' + message)

        response = response_success_json()
        self.write(response)


class WeiboNewsDataHandler(RequestHandler):

    def post(self, *args, **kwargs):
        item_list_json = self.get_argument('news_list')
        item_list = json.loads(item_list_json)
        db = get_mongodb246()
        for i in item_list:
            weibo = db.weibo.find_one({'id': i['status']['id']})
            if weibo:
                logging.warning('Drop item: already exists')
                continue
            i['id'] = i['status']['id']
            i['procedure'] = 0
            db.weibo.insert(i)
        self.write(response_success_json())


class VideoViewHandler(RequestHandler):
    def get(self, *args, **kwargs):
        db = get_mongodb()
        count = db.news.find({'status': 4}).count()
        skip = random.randint(0, count-11)
        videos_data = db.news.find({'status': 4}).skip(skip).limit(10)
        html_code_list = list()
        for j in videos_data:
            item = dict()
            item['url'] = j['key']
            item['title'] = j['title']
            item['pub_time'] = j['publish_time']
            item['docid'] = item['url']
            item['content_html'] = j['content_html']
            content_list = extractor(j['content_html'])
            item['content'] = json.dumps(change_text_txt(content_list))
            html = ''
            html += '<center><h2>' + item['title'] + '</h2></center>'
            html += '<p>' + item['pub_time'] + '</p>'
            # html += '<p>' + item['pub_name'] + '</p>'
            content = json.loads(item['content'])
            if not content:
                continue
            for i in content:
                if 'txt' in i:
                    html += '<p>&nbsp&nbsp&nbsp&nbsp&nbsp' + i['txt'] + '</p>'
                elif 'img' in i:
                    html += '<center><img src="' + i['img'].encode('utf8') + '"></center>'
                elif 'video' in i:
                    html += '<center><video controls="controls" src="%s"></center>' % i['video'].encode('utf8')
            html += '<p>' + '-'*100 + '</p>'
            html_code_list.append(html)
        self.render('item.html', data=html_code_list)
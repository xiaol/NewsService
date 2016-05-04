# coding=utf-8
import logging
import json

from tornado.web import RequestHandler, asynchronous

from operations.appitem_ops import AppItemOperation
from utils.response_handler import response_fail_json, response_success_json


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
        ret, message = AppItemOperation().create_app_item(args)
        if ret:
            response = response_success_json(ret_message=message)
        else:
            response = response_fail_json(ret_message=message)
            logging.warning(response)
            logging.warning('params: ' + json.dumps(args))
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
                params['summary'] = i['summary']
                if len(params['summary']) <= 60:
                    params['title'] = params['summary']
            else:
                params['summary'] = ''
            params['detail_html'] = params['summary']
            if 'pictureUrl' in i and i['pictureUrl']:
                for j in i['pictureUrl']:
                    params['detail_html'] += '<img src= %s />' % j
            if 'link' in i and i['link']:
                params['link'] = i['link']
            ret, message = AppItemOperation().create_app_item(params)
            if not ret:
                logging.warning('params: ' + json.dumps(i))
                logging.warning('Warning message: ' + message)

        response = response_success_json()
        self.write(response)

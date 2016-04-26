# coding=utf-8
import json

from tornado.web import RequestHandler, asynchronous

from operations.appitem_ops import AppItemOperation
from utils.response_handler import response_fail_json, response_success_json


class NewsDataHandler(RequestHandler):
    def post(self, *args, **kwargs):
        args = self.request.arguments
        for i in args:
            args[i] = args[i][0]
        print args
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
        self.write(response)

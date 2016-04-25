import json

from tornado.web import RequestHandler, asynchronous

from operations.appitem_ops import AppItemOperation


class NewsDataHandler(RequestHandler):
    def post(self, *args, **kwargs):
        data = self.request.body
        try:
            news = json.loads(data)
        except Exception, e:
            print e
            return
        print news
        # for i in news_list:
        ret = AppItemOperation().create_app_item(news)
        if ret:
            self.write({"result": "Success!"})
        else:
            self.write({"result": 'Failed!', "message": "invalid params"})


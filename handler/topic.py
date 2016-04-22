from tornado.web import RequestHandler
import json

from utils.utility import news_verify, get_mongodb


class NewsDataHandler(RequestHandler):
    def post(self, *args, **kwargs):
        # data = self.get_argument('data')
        data = self.request.body
        try:
            news_list = json.loads(data)
        except Exception, e:
            print e
            self.write('{"result": "Failed!"}')
        db = get_mongodb()
        print news_list
        for i in news_list:
            verify = news_verify(i)
            if verify:
                db.news.insert(i)
                print 1
            else:
                continue

        self.write('{"result": "Success!"}')
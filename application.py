import os

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options
from tornado.web import RequestHandler

from handler.topic import NewsDataHandler, JikeNewsDataHandler, VideoViewHandler

class Application(tornado.web.Application):
    def __init__(self):

        settings = {
            'template_path': 'template',
            'static_path': os.path.join(os.path.dirname(__file__), 'template')
        }

        handlers = [
            (r'/news', NewsDataHandler),
            # (r'/jike_news', JikeNewsDataHandler),
            # (r'/videos', VideoViewHandler),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(9000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
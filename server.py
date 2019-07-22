import tornado.ioloop
import tornado.web

from definition.handlers.api_handler import ApiHandler
from definition.handlers.index_handlers import IndexHandler


def make_app():
    return tornado.web.Application([
        (r"/api/definition", ApiHandler),
        (r"/", IndexHandler)

    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

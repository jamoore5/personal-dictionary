import tornado.ioloop
import tornado.web

from definition.handlers.api_handler import ApiHandler
from definition.handlers.frontend_handlers import CreateHandler, IndexHandler, EditHandler


def make_app():
    return tornado.web.Application([
        (r"/api/definition", ApiHandler),
        (r"/definition/create", CreateHandler),
        (r"/definition", EditHandler),
        (r"/", IndexHandler)

    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

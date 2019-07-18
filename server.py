import tornado.ioloop
import tornado.web

from definition_handler import DefinitionHandler


def make_app():
    return tornado.web.Application([
        (r"/definition", DefinitionHandler)
    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

import tornado.web

from api_adapter import ApiAdapter


class CreateHandler(tornado.web.RequestHandler):
    async def get(self):
        self.render("../views/create.html")


class EditHandler(tornado.web.RequestHandler):
    async def get(self):
        word = self.get_argument('word')
        adapter = ApiAdapter()
        definition = await adapter.fetch("api/definition?word=" + word)
        self.render("../views/edit.html", definition=definition)


class IndexHandler(tornado.web.RequestHandler):
    async def get(self):
        adapter = ApiAdapter()
        definitions = await adapter.fetch("api/definition")
        self.render("../views/index.html", definitions=definitions)

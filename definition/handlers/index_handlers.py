import tornado.web

from api_adapter import ApiAdapter


class IndexHandler(tornado.web.RequestHandler):
    async def get(self):
        show_links = self.get_argument('show_links', False)
        adapter = ApiAdapter()
        definitions = await adapter.fetch("api/definition")
        self.render("../views/index.html", definitions=definitions, show_links=show_links)

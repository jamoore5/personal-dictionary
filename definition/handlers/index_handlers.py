import tornado.web
import random

from api_adapter import ApiAdapter

quotes = [
    {"quote": "Few activities are as delightful as learning new vocabulary.", "author(s)": "Tim Gunn"},
    {"quote": "I collect words--they are sweets in the mouth of sound.", "author(s)": "Sally Gardner, Maggot Moon "}
]



class IndexHandler(tornado.web.RequestHandler):
    async def get(self):
        show_links = self.get_argument('show_links', False)
        adapter = ApiAdapter()
        definitions = await adapter.fetch("api/definition")
        self.render("../views/index.html", definitions=definitions, show_links=show_links, quote=random.choice(quotes))


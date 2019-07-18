import tornado.web
import json

from mongo_adapter import MongoAdapter, DuplicateKeyError


class DefinitionHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.adapter = MongoAdapter()
        self.adapter.create_unique_word_index()

    def write_response(self, response):
        self.write({"data": response})

    def get(self):
        word = self.get_argument('word', None)
        if word is None:
            definitions = self.adapter.find_all()
        else:
            definitions = self.adapter.find(word)

        if definitions is None:
            self.set_status(404)
        else:
            self.write_response(definitions)

    def post(self):
        definition = json.loads(self.request.body.decode('utf-8'))
        try:
            self.adapter.insert(definition)
        except DuplicateKeyError:
            self.set_status(303)

        self.write_response(definition)

    def delete(self):
        word = self.get_argument('word')
        self.adapter.delete(word)

import tornado.web
import json

from database_adapter import DatabaseAdapter, DuplicateError
from definition.definition import Definition, ValidationError


class ApiHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.adapter = DatabaseAdapter()
        self.adapter.create_unique_word_index()

    def write_response(self, response):
        self.write({"data": response})

    def request_body(self):
        return json.loads(self.request.body.decode('utf-8'))

    def definition(self):
        try:
            definition = Definition(self.request_body())
        except ValidationError as e:
            self.set_status(400)
            self.write({'error': str(e)})
            return

        return definition.to_dict()

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
        definition = self.definition()
        if definition is None:
            return

        try:
            self.adapter.insert(definition)
        except DuplicateError:
            self.set_status(303)

        self.write_response(definition)

    def patch(self):
        word = self.get_argument('word')
        definition = self.definition()
        if definition is None:
            return

        self.adapter.update(word, definition)

        definition = self.adapter.find(word)
        self.write_response(definition)

    def put(self):
        word = self.get_argument('word')
        definition = self.definition()
        if definition is None:
            return

        self.adapter.replace(word, definition)

        self.write_response(definition)

    def delete(self):
        word = self.get_argument('word')
        self.adapter.delete(word)

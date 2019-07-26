from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
import json

from database_adapter import DatabaseAdapter, DuplicateError
from definition.handlers.api_handler import ApiHandler


class MockError(Exception):
    pass


class MockDatabaseAdapter(object):
    def __init__(self, word=None, definition=None):
        self.word = word
        self.definition = definition

        self.dictionary = {
            'personal': {'word': 'personal', 'pronunciation': 'per·son·al',
                         'definition': 'of, affecting, or belonging to a particular person rather than to anyone else'},
            'dictionary': {'word': 'dictionary', 'pronunciation': 'dic·tion·ar·y',
                           'definition': 'a book or electronic resource that lists the words of a language'}
        }

        DatabaseAdapter.find_all = self.mock_find_all
        DatabaseAdapter.find = self.mock_find
        DatabaseAdapter.insert = self.mock_insert
        DatabaseAdapter.update = self.mock_update
        DatabaseAdapter.replace = self.mock_replace
        DatabaseAdapter.delete = self.mock_delete

    def mock_find_all(self):
        return list(self.dictionary.values())

    def mock_find(self, word):
        if word != self.word:
            raise MockError(f"Expected word '{self.word}', but got '{word}'")

        if word not in list(self.dictionary.keys()):
            return None
        else:
            return self.dictionary[word]

    def mock_insert(self, definition):
        if definition != self.definition:
            raise MockError(f"Expected word '{self.definition}', but got '{definition}'")

        if definition in list(self.dictionary.values()):
            raise DuplicateError

        return None

    def mock_update(self, word, _definition):
        if word != self.word:
            raise MockError(f"Expected word '{self.word}', but got '{word}'")
        return

    def mock_replace(self, word, _definition):
        if word != self.word:
            raise MockError(f"Expected word '{self.word}', but got '{word}'")
        return

    def mock_delete(self, word):
        if word != self.word:
            raise MockError(f"Expected word '{self.word}', but got '{word}'")
        return


class TestApiHandler(AsyncHTTPTestCase):
    def setup_class(ApiHandlerTest):
        def mock_create_unique_word_index(_self):
            return

        DatabaseAdapter.create_unique_word_index = mock_create_unique_word_index

    def get_app(self):
        self.app = Application([('/', ApiHandler)])
        return self.app

    def test_get_all_definitions(self):
        MockDatabaseAdapter()

        response = self.fetch('/', method='GET')
        assert response.code == 200

        definitions = json.loads(response.body.decode('utf-8'))['data']

        assert len(definitions) == 2
        assert sorted(list({d['word'] for d in definitions})) == sorted(['personal', 'dictionary'])

    def test_get_word_not_in_dictionary(self):
        MockDatabaseAdapter('random')

        response = self.fetch('/?word=random', method='GET')

        assert response.code == 404

    def test_get_word_in_dictionary(self):
        MockDatabaseAdapter('dictionary')

        response = self.fetch('/?word=dictionary', method='GET')

        assert response.code == 200

        definition = json.loads(response.body.decode('utf-8'))['data']
        assert list(definition.values()) == ['dictionary', 'dic·tion·ar·y',
                                             'a book or electronic resource that lists the words of a language']

    def test_post_word(self):
        MockDatabaseAdapter('foo',
                            {'word': 'foo', 'pronunciation': 'foo',
                             'definition': 'term used by programmers as a placeholder for a value that can change'})

        body = {'word': 'foo', 'pronunciation': 'foo',
                'definition': 'term used by programmers as a placeholder for a value that can change'}

        response = self.fetch('/', method='POST', body=json.dumps(body).encode('utf-8'))

        assert response.code == 200

    def test_post_invalid_word(self):
        body = {'pronunciation': 'foo',
                'definition': 'term used by programmers as a placeholder for a value that can change'}

        response = self.fetch('/', method='POST', body=json.dumps(body).encode('utf-8'))

        assert response.code == 400
        assert json.loads(response.body.decode('utf-8')) == {'error': "Definition missing required field 'word'"}

    def test_post_strips_whitespace_off_word(self):
        MockDatabaseAdapter('foo',
                            {'word': 'foo', 'pronunciation': 'foo',
                             'definition': 'term used by programmers as a placeholder for a value that can change'})
        body = {'word': '  foo  ', 'pronunciation': 'foo',
                'definition': 'term used by programmers as a placeholder for a value that can change'}

        response = self.fetch('/', method='POST', body=json.dumps(body).encode('utf-8'))

        assert response.code == 200

    def test_post_duplicate_word(self):
        MockDatabaseAdapter('dictionary',
                            {'word': 'dictionary', 'pronunciation': 'dic·tion·ar·y',
                             'definition': 'a book or electronic resource that lists the words of a language'})

        body = {'word': 'dictionary', 'pronunciation': 'dic·tion·ar·y',
                'definition': 'a book or electronic resource that lists the words of a language'}

        response = self.fetch('/', method='POST', body=json.dumps(body).encode('utf-8'))

        assert response.code == 303

    def test_patch_word(self):
        MockDatabaseAdapter('dictionary')

        body = {'word': 'dictionary', 'pronunciation': 'dic·tion·ar·y',
                'definition': 'a book or electronic resource that lists the words of a language'}

        response = self.fetch('/?word=dictionary', method='PATCH', body=json.dumps(body).encode('utf-8'))

        assert response.code == 200

    def test_patch_invalid_word(self):
        body = {'pronunciation': 'dic·tion·ar·y',
                'definition': 'a book or electronic resource that lists the words of a language'}

        response = self.fetch('/?word=dictionary', method='PATCH', body=json.dumps(body).encode('utf-8'))

        assert response.code == 400
        assert json.loads(response.body.decode('utf-8')) == {'error': "Definition missing required field 'word'"}

    def test_patch_strips_whitespace_off_word(self):
        MockDatabaseAdapter('dictionary')

        body = {'word': '   dictionary  ', 'pronunciation': 'dic·tion·ar·y',
                'definition': 'a book or electronic resource that lists the words of a language'}

        response = self.fetch('/?word=dictionary', method='PATCH', body=json.dumps(body).encode('utf-8'))

        assert response.code == 200

    def test_put_word(self):
        MockDatabaseAdapter('dictionary')

        body = {'word': 'dictionary', 'pronunciation': 'dic·tion·ar·y',
                'definition': 'a book or electronic resource that lists the words of a language'}

        response = self.fetch('/?word=dictionary', method='PUT', body=json.dumps(body).encode('utf-8'))

        assert response.code == 200

    def test_put_invalid_word(self):
        body = {'pronunciation': 'dic·tion·ar·y',
                'definition': 'a book or electronic resource that lists the words of a language'}

        response = self.fetch('/?word=dictionary', method='PUT', body=json.dumps(body).encode('utf-8'))

        assert response.code == 400
        assert json.loads(response.body.decode('utf-8')) == {'error': "Definition missing required field 'word'"}

    def test_put_strips_whitespace_off_word(self):
        MockDatabaseAdapter('dictionary')

        body = {'word': '   dictionary  ', 'pronunciation': 'dic·tion·ar·y',
                'definition': 'a book or electronic resource that lists the words of a language'}

        response = self.fetch('/?word=dictionary', method='PUT', body=json.dumps(body).encode('utf-8'))

        assert response.code == 200

    def test_delete_word(self):
        MockDatabaseAdapter('dictionary')

        response = self.fetch('/?word=dictionary', method='DELETE')

        assert response.code == 200

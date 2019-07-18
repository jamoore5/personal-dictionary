from pymongo import MongoClient, ASCENDING
import pymongo.errors

import os

class DuplicateKeyError(Exception):
    pass


class MongoAdapter:
    def __init__(self):
        url = os.environ.get('MONGODB_URL')
        client = MongoClient(url)
        db = client.test
        self.defintion_collection = db.definitions

    def create_unique_word_index(self):
        self.defintion_collection.create_index([('word', ASCENDING)], unique=True)

    def insert(self, definition):
        try:
            self.defintion_collection.insert_one(definition)
        except pymongo.errors.DuplicateKeyError:
            raise DuplicateKeyError
        finally:
            del definition['_id']

    def delete(self, word):
        self.defintion_collection.delete_one({"word": word})

    def find(self, word):
        return self.defintion_collection.find_one({"word": word}, {'_id': False})

    def find_all(self):
        return list(self.defintion_collection.find(None, {'_id': False}))
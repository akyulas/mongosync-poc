import pymongo

class MongoAdapter:
    def __init__(self, connection_string, db_name, collection_names):
        self.client = pymongo.MongoClient(connection_string)
        self.db_name = db_name
        self.collection_names = collection_names

    def db_write(self, collection_name, entry):
        db = self.client[self.db_name]
        collection = db[collection_name]
        collection.insert_one(entry)
    
    def db_drop(self):
        db = self.client[self.db_name]
        for collection_name in self.collection_names:
            collection = db[collection_name]
            collection.drop()
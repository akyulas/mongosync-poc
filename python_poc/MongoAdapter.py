import pymongo

class MongoAdapter:
    def __init__(self, connection_string):
        self.client = pymongo.MongoClient(connection_string)

    def db_write(self, db_name, collection_name, entry):
        db = self.client[db_name]
        collection = db[collection_name]
        collection.insert_one(entry)
    
    def db_drop(self, db_name, collection_names):
        db = self.client[db_name]
        for collection_name in collection_names:
            collection = db[collection_name]
            collection.drop()
import argparse
from MongoAdapter import MongoAdapter
import random, string
from random import randrange
import uuid

# CONNECTION STRINGS
REPLICA_SET_CLUSTER_1_CONNECTION_STRING = 'mongodb://localhost:20010,localhost:20011,localhost:20012/'
REPLICA_SET_CLUSTER_2_CONNECTION_STRING = 'mongodb://localhost:20013,localhost:20014,localhost:20015/'
REPLICA_SET_CLUSTER_3_CONNECTION_STRING = 'mongodb://localhost:20016,localhost:20017,localhost:20018/'

# DB NAME AND COLLECTION_NAMES, etc
REPLICA_TEST_DB = "test"
REPLICA_COLLECTION_NAMES = ["collection_1", "collection_2", "collection_3", "collection_4", "collection_5"]
DC_DICT = {
    0: "DC_1",
    1: "DC_2",
    2: "DC_3"
}

# INITIALIZING THE ADAPTER
replica_adapters = [
    MongoAdapter(REPLICA_SET_CLUSTER_1_CONNECTION_STRING),
    MongoAdapter(REPLICA_SET_CLUSTER_2_CONNECTION_STRING),
    MongoAdapter(REPLICA_SET_CLUSTER_3_CONNECTION_STRING)
]

def write_to_db():
    def random_uuid(suffix):
        return str(uuid.uuid4()) + "_" + str(suffix)
    def random_word(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    random_dc = randrange(3)
    for replica_adapter in replica_adapters:
        for collection_name in REPLICA_COLLECTION_NAMES:
            replica_entry = {
                "dc": DC_DICT[random_dc],
                "random_id": random_uuid(random_dc),
                "random_word": random_word(10)
            }
            replica_adapter.db_write(REPLICA_TEST_DB, collection_name, replica_entry)

def drop_db():
    for replica_adapter in replica_adapters:
        replica_adapter.db_drop(REPLICA_TEST_DB, REPLICA_COLLECTION_NAMES)

# MAIN FUNCTION
if __name__=="__main__":
    # INITIALIZE PARSER
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--drop", help = "DROP REPLICA SET DB AND COLLECTIONS", action="store_true")
    parser.add_argument("-w", "--write", help = "START WRITING TO DB", action="store_true")

    # PARSING ARGUMENT_AND_PERFORM_ACTION
    args = parser.parse_args()
    if args.drop:
        drop_db()
    elif args.write:
        write_to_db()
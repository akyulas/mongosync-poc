import argparse
from MongoAdapter import MongoAdapter
import random, string
from random import randrange
import uuid
import time
import sys

# CONNECTION STRINGS
REPLICA_SET_CLUSTER_1_CONNECTION_STRING = 'mongodb://localhost:20010,localhost:20011,localhost:20012/'
REPLICA_SET_CLUSTER_2_CONNECTION_STRING = 'mongodb://localhost:20013,localhost:20014,localhost:20015/'
REPLICA_SET_CLUSTER_3_CONNECTION_STRING = 'mongodb://localhost:20016,localhost:20017,localhost:20018/'
MONGOS_CONNECTION_STRING = 'mongodb://localhost:30000/'

# DB NAME AND COLLECTION_NAMES, etc
REPLICA_TEST_DB = "replica_test"
REPLICA_COLLECTION_NAMES = [
    "collection_1",
    "collection_2",
    "collection_3",
    "collection_4",
    "collection_5"
]
SHARD_TEST_DB = 'shard_test'
SHARD_COLLECTION_NAMES = [
    "collection_4",
    "collection_5"
]
DC_DICT = {
    0: "DC_1",
    1: "DC_2",
    2: "DC_3"
}

# INITIALIZING THE ADAPTER
REPLICA_ADAPTERS = [
    MongoAdapter(REPLICA_SET_CLUSTER_1_CONNECTION_STRING),
    MongoAdapter(REPLICA_SET_CLUSTER_2_CONNECTION_STRING),
    MongoAdapter(REPLICA_SET_CLUSTER_3_CONNECTION_STRING)
]
SHARD_ADAPTERS = [
    MongoAdapter(MONGOS_CONNECTION_STRING)
]

# CONSTANT RELATED TO WRITE
WRITE_BATCH = 2
SLEEP_BETWEEN_BATCH = 5

def write_to_db(is_shard):
    def random_uuid(suffix):
        return str(uuid.uuid4()) + "_" + str(suffix)
    def random_word(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    def generate_random_entry(random_dc):
        return {
            "dc": DC_DICT[random_dc],
            "random_id": random_uuid(random_dc),
            "random_word": random_word(10)
         }
    def actual_write_to_db(adapters, db, collection_names):
        for adapter in adapters:
            for collection_name in collection_names:
                random_dc = randrange(3)
                entry = generate_random_entry(random_dc)
                adapter.db_write(db, collection_name, entry)
    while True:
        print("Starting to write to Mongo")
        for _ in range(WRITE_BATCH):
            if is_shard:
                actual_write_to_db(SHARD_ADAPTERS, SHARD_TEST_DB, SHARD_COLLECTION_NAMES)
            else:
                actual_write_to_db(REPLICA_ADAPTERS, REPLICA_TEST_DB, REPLICA_COLLECTION_NAMES)
        print(f"Sleeping for {SLEEP_BETWEEN_BATCH}s")
        time.sleep(SLEEP_BETWEEN_BATCH)

def drop_db(is_shard):
    def actual_drop_from_db(adapters, db, collection_names):
        for adapter in adapters:
            adapter.db_drop(db, collection_names)

    if is_shard:
        actual_drop_from_db(SHARD_ADAPTERS, SHARD_TEST_DB, SHARD_COLLECTION_NAMES)
        print("Collections has been dropped from sharded cluster")
    else:
        actual_drop_from_db(REPLICA_ADAPTERS, REPLICA_TEST_DB, REPLICA_COLLECTION_NAMES)
        print("Collections has been dropped from replica cluster")

# MAIN FUNCTION
if __name__=="__main__":
    try:
        # INITIALIZE PARSER
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--drop", help = "DROP REPLICA SET DB AND COLLECTIONS", action="store_true")
        parser.add_argument("-w", "--write", help = "START WRITING TO DB", action="store_true")
        parser.add_argument("-s", "--shard", help = "PERFORM OPERATIONS ON SHARD", action="store_true")

        # PARSING ARGUMENT_AND_PERFORM_ACTION
        args = parser.parse_args()
        if args.drop:
            drop_db(args.shard)
        elif args.write:
            write_to_db(args.shard)
    except KeyboardInterrupt:
        print("Exiting")
        sys.exit(0)
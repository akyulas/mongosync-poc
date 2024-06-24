import argparse
from MongoAdapter import MongoAdapter
import random, string
from random import randrange
import uuid
import time
import sys
import datetime

# CONNECTION STRINGS
REPLICA_SET_CLUSTER_1_CONNECTION_STRING = 'mongodb://localhost:20010,localhost:20011,localhost:20012/'
REPLICA_SET_CLUSTER_2_CONNECTION_STRING = 'mongodb://localhost:20013,localhost:20014,localhost:20015/'
REPLICA_SET_CLUSTER_3_CONNECTION_STRING = 'mongodb://localhost:20016,localhost:20017,localhost:20018/'
MONGOS_CONNECTION_STRING = 'mongodb://localhost:30000,localhost:30001,localhost:30002/'

# DB NAME AND COLLECTION_NAMES, etc
REPLICA_TEST_DB = "replica_test"
REPLICA_COLLECTION_NAMES = [
    "collection_1",
    "collection_2",
    "collection_3",
    "collection_4",
    "collection_5"
]
SHARD_TEST_DB = 'replica_test'
ALTERNATE_SHARD_TEST_DB = 'shard_test'
ALL_SHARD_COLLECTION_NAMES = [
    "collection_1",
    "collection_2",
    "collection_3",
    "collection_4",
    "collection_5"
]
SHARD_COLLECTION_NAMES = [
    "collection_4",
    "collection_5"
]
DC_DICT = {
    0: "DC_1",
    1: "DC_2",
    2: "DC_3"
}

# CONSTANT RELATED TO WRITE
WRITE_BATCH = 2
SLEEP_BETWEEN_BATCH = 5

def write_to_db(is_both, is_shard):
    def random_uuid(suffix):
        return str(uuid.uuid4()) + "_" + str(suffix)
    def random_word(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
    def generate_source():
        if is_both:
            return 'both'
        elif is_shard:
            return 'shard'
        return 'replica'
    def generate_random_entry(random_dc):
        return {
            "dc": DC_DICT[random_dc],
            "random_id": random_uuid(random_dc),
            "random_word": random_word(10),
            "created_time": datetime.datetime.utcnow(),
            'source': generate_source()
         }
    def actual_write_to_db(adapters, insert_same_entry_to_all_db):
        random_dc = randrange(3)
        entry = generate_random_entry(random_dc)
        for adapter in adapters:
            for collection_name in adapter.collection_names:
                if not insert_same_entry_to_all_db:
                    random_dc = randrange(3)
                    entry = generate_random_entry(random_dc)
                adapter.db_write(collection_name, entry)
    while True:
        print("Starting to write to Mongo")
        for _ in range(WRITE_BATCH):
            insert_same_entry_to_all_db = is_both
            actual_write_to_db(adapters, insert_same_entry_to_all_db)
        print(f"Sleeping for {SLEEP_BETWEEN_BATCH}s")
        time.sleep(SLEEP_BETWEEN_BATCH)

def drop_db():
    for adapter in adapters:
        adapter.db_drop()
    print("Collections has been dropped")
    
def create_adapters(is_both, is_shard, is_alternate, is_all):
    if is_all or is_both:
        shard_collection_names = ALL_SHARD_COLLECTION_NAMES
    else:
        shard_collection_names = SHARD_COLLECTION_NAMES
    if is_alternate:
        shard_db = ALTERNATE_SHARD_TEST_DB
    else:
        shard_db = SHARD_TEST_DB
    if is_both:
        return [
            MongoAdapter(MONGOS_CONNECTION_STRING, shard_db, shard_collection_names),
            MongoAdapter(REPLICA_SET_CLUSTER_1_CONNECTION_STRING, REPLICA_TEST_DB, REPLICA_COLLECTION_NAMES),
        ]
    if not is_shard:
        return [
            MongoAdapter(REPLICA_SET_CLUSTER_1_CONNECTION_STRING, REPLICA_TEST_DB, REPLICA_COLLECTION_NAMES),
            MongoAdapter(REPLICA_SET_CLUSTER_2_CONNECTION_STRING, REPLICA_TEST_DB, REPLICA_COLLECTION_NAMES),
            MongoAdapter(REPLICA_SET_CLUSTER_3_CONNECTION_STRING, REPLICA_TEST_DB, REPLICA_COLLECTION_NAMES)
            ]
    return [
        MongoAdapter(MONGOS_CONNECTION_STRING, shard_db, shard_collection_names)
        ]
# MAIN FUNCTION
if __name__=="__main__":
    try:
        # INITIALIZE PARSER
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--drop", help = "DROP REPLICA SET DB AND COLLECTIONS", action="store_true")
        parser.add_argument("-w", "--write", help = "START WRITING TO DB", action="store_true")
        parser.add_argument("-s", "--shard", help = "PERFORM OPERATIONS ON SHARD", action="store_true")
        parser.add_argument("-a", "--alternate", help = "USE ALTERNATE DB FOR SHARDING", action="store_true")
        parser.add_argument("--all", help = "USE ALL COLLECTION NAMES FOR SHARDING", action="store_true")
        parser.add_argument("-b", "--both", help="WRITE TO BOTH REPLICA SET AND SHARD", action='store_true')
        # PARSING ARGUMENT_AND_PERFORM_ACTION
        args = parser.parse_args()
        # INITIALIZE THE ADAPTERS
        adapters = create_adapters(args.both, args.shard, args.alternate, args.all)
        if args.drop:
            drop_db()
        elif args.write:
            write_to_db(args.both, args.shard)
    except KeyboardInterrupt:
        print("Exiting")
        sys.exit(0)
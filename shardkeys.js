use replica_test;
sh.shardCollection("replica_test.collection_4", { "dc": 1, "random_id": 1 });
sh.shardCollection("replica_test.collection_5", { "dc": 1, "random_id": 1 });
use shard_test;
sh.shardCollection("shard_test.collection_4", { "dc": 1, "random_id": 1 });
sh.shardCollection("shard_test.collection_5", { "dc": 1, "random_id": 1 });
docker network create mongo-demo-network
echo "Starting config server"
docker compose -f config_server/docker-compose.yaml up -d
sleep 3
docker exec -it configsvr1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"config_rs\",
    configsvr: true,
    members: [
        { _id: 0, host: \"configsvr1:27017\" },
        { _id: 1, host: \"configsvr2:27017\" },
        { _id: 2, host: \"configsvr3:27017\" }
    ]
})"
echo "Starting sharded cluster"
docker compose -f shard_server1/docker-compose.yaml up -d
docker compose -f shard_server2/docker-compose.yaml up -d
docker compose -f shard_server3/docker-compose.yaml up -d
sleep 3
docker exec -it shardsvr1_1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"shard1_rs\",
    members: [
      { _id : 0, host : \"shardsvr1_1:27017\" },
      { _id : 1, host : \"shardsvr1_2:27017\" },
      { _id : 2, host : \"shardsvr1_3:27017\" }
    ]
})"
docker exec -it shardsvr2_1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"shard2_rs\",
    members: [
      { _id : 0, host : \"shardsvr2_1:27017\" },
      { _id : 1, host : \"shardsvr2_2:27017\" },
      { _id : 2, host : \"shardsvr2_3:27017\" }
    ]
})"
docker exec -it shardsvr3_1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"shard3_rs\",
    members: [
      { _id : 0, host : \"shardsvr3_1:27017\" },
      { _id : 1, host : \"shardsvr3_2:27017\" },
      { _id : 2, host : \"shardsvr3_3:27017\" }
    ]
})"
echo "Starting replica set"
docker compose -f replica_server1/docker-compose.yaml up -d
docker compose -f replica_server2/docker-compose.yaml up -d
docker compose -f replica_server3/docker-compose.yaml up -d
sleep 3
docker exec -it replicasvr1_1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"replica1_rs\",
    members: [
      { _id : 0, host : \"replicasvr1_1:27017\" },
      { _id : 1, host : \"replicasvr1_2:27017\" },
      { _id : 2, host : \"replicasvr1_3:27017\" }
    ]
})"
docker exec -it replicasvr2_1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"replica2_rs\",
    members: [
      { _id : 0, host : \"replicasvr2_1:27017\" },
      { _id : 1, host : \"replicasvr2_2:27017\" },
      { _id : 2, host : \"replicasvr2_3:27017\" }
    ]
})"
docker exec -it replicasvr3_1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"replica3_rs\",
    members: [
      { _id : 0, host : \"replicasvr3_1:27017\" },
      { _id : 1, host : \"replicasvr3_2:27017\" },
      { _id : 2, host : \"replicasvr3_3:27017\" }
    ]
})"
echo "Starting mongos"
docker compose -f mongo_router/docker-compose.yaml up -d
docker compose -f mongo_router-2/docker-compose.yaml up -d
docker compose -f mongo_router-3/docker-compose.yaml up -d
sleep 5
docker exec -it mongos1 mongosh --port 27017 --eval "sh.addShard(\"shard1_rs/shardsvr1_1:27017,shardsvr1_2:27017,shardsvr1_3:27017\")"
docker exec -it mongos1 mongosh --port 27017 --eval "sh.addShard(\"shard2_rs/shardsvr2_1:27017,shardsvr2_2:27017,shardsvr2_3:27017\")"
docker exec -it mongos1 mongosh --port 27017 --eval "sh.addShard(\"shard3_rs/shardsvr3_1:27017,shardsvr3_2:27017,shardsvr3_3:27017\");"
docker exec -it mongos2 mongosh --port 27017 --eval "sh.addShard(\"shard1_rs/shardsvr1_1:27017,shardsvr1_2:27017,shardsvr1_3:27017\")"
docker exec -it mongos2 mongosh --port 27017 --eval "sh.addShard(\"shard2_rs/shardsvr2_1:27017,shardsvr2_2:27017,shardsvr2_3:27017\")"
docker exec -it mongos2 mongosh --port 27017 --eval "sh.addShard(\"shard3_rs/shardsvr3_1:27017,shardsvr3_2:27017,shardsvr3_3:27017\");"
docker exec -it mongos3 mongosh --port 27017 --eval "sh.addShard(\"shard1_rs/shardsvr1_1:27017,shardsvr1_2:27017,shardsvr1_3:27017\")"
docker exec -it mongos3 mongosh --port 27017 --eval "sh.addShard(\"shard2_rs/shardsvr2_1:27017,shardsvr2_2:27017,shardsvr2_3:27017\")"
docker exec -it mongos3 mongosh --port 27017 --eval "sh.addShard(\"shard3_rs/shardsvr3_1:27017,shardsvr3_2:27017,shardsvr3_3:27017\");"

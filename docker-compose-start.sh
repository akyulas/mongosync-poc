docker network create mongo-demo-network
echo "Starting config server"
docker compose -f config_server/docker-compose.yaml up -d
sleep 3
docker exec -it configsvr1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"config_rs\",
    configsvr: true,
    members: [
        { _id: 0, host: \"host.docker.internal:10001\" },
        { _id: 1, host: \"host.docker.internal:10002\" },
        { _id: 2, host: \"host.docker.internal:10003\" }
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
      { _id : 0, host : \"host.docker.internal:20001\" },
      { _id : 1, host : \"host.docker.internal:20002\" },
      { _id : 2, host : \"host.docker.internal:20003\" }
    ]
})"
docker exec -it shardsvr2_1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"shard2_rs\",
    members: [
      { _id : 0, host : \"host.docker.internal:20004\" },
      { _id : 1, host : \"host.docker.internal:20005\" },
      { _id : 2, host : \"host.docker.internal:20006\" }
    ]
})"
docker exec -it shardsvr3_1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"shard3_rs\",
    members: [
      { _id : 0, host : \"host.docker.internal:20007\" },
      { _id : 1, host : \"host.docker.internal:20008\" },
      { _id : 2, host : \"host.docker.internal:20009\" }
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
      { _id : 0, host : \"host.docker.internal:20010\" },
      { _id : 1, host : \"host.docker.internal:20011\" },
      { _id : 2, host : \"host.docker.internal:20012\" }
    ]
})"
docker exec -it replicasvr2_1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"replica2_rs\",
    members: [
      { _id : 0, host : \"host.docker.internal:20013\" },
      { _id : 1, host : \"host.docker.internal:20014\" },
      { _id : 2, host : \"host.docker.internal:20015\" }
    ]
})"
docker exec -it replicasvr3_1 mongosh --port 27017 --eval "rs.initiate({
    _id: \"replica3_rs\",
    members: [
      { _id : 0, host : \"host.docker.internal:20016\" },
      { _id : 1, host : \"host.docker.internal:20017\" },
      { _id : 2, host : \"host.docker.internal:20018\" }
    ]
})"
echo "Starting mongos"
docker compose -f mongo_router/docker-compose.yaml up -d
docker compose -f mongo_router-2/docker-compose.yaml up -d
docker compose -f mongo_router-3/docker-compose.yaml up -d
sleep 5
docker exec -it mongos1 mongosh --port 27017 --eval "sh.addShard(\"shard1_rs/host.docker.internal:20001,host.docker.internal:20002,host.docker.internal:20003\")"
docker exec -it mongos1 mongosh --port 27017 --eval "sh.addShard(\"shard2_rs/host.docker.internal:20004,host.docker.internal:20005,host.docker.internal:20006\")"
docker exec -it mongos1 mongosh --port 27017 --eval "sh.addShard(\"shard3_rs/host.docker.internal:20007,host.docker.internal:20008,host.docker.internal:20009\")"
docker exec -it mongos2 mongosh --port 27017 --eval "sh.addShard(\"shard1_rs/host.docker.internal:20001,host.docker.internal:20002,host.docker.internal:20003\")"
docker exec -it mongos2 mongosh --port 27017 --eval "sh.addShard(\"shard2_rs/host.docker.internal:20004,host.docker.internal:20005,host.docker.internal:20006\")"
docker exec -it mongos2 mongosh --port 27017 --eval "sh.addShard(\"shard3_rs/host.docker.internal:20007,host.docker.internal:20008,host.docker.internal:20009\")"
docker exec -it mongos3 mongosh --port 27017 --eval "sh.addShard(\"shard1_rs/host.docker.internal:20001,host.docker.internal:20002,host.docker.internal:20003\")"
docker exec -it mongos3 mongosh --port 27017 --eval "sh.addShard(\"shard2_rs/host.docker.internal:20004,host.docker.internal:20005,host.docker.internal:20006\")"
docker exec -it mongos3 mongosh --port 27017 --eval "sh.addShard(\"shard3_rs/host.docker.internal:20007,host.docker.internal:20008,host.docker.internal:20009\")"
docker exec -i mongos1 bash -c 'mongosh' < shardkeys.js

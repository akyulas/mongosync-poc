## Sharding in MongoDB using docker

You can set-up sharding in MongoDB by creating a cluster of mongo instances consisting of the below components:
1. Config servers
2. Shard servers
3. Mongo routers

All the above instances are created using docker containers. In this repo we create 1 config replica set, 2 shard replica sets and 1 mongo router. Each replica set contains 3 mongo instances. 


### Pre-requisites
1. Install docker based on your platform.
2. Install mongodb from https://www.mongodb.com/docs/manual/installation/

### Config servers
Run the below docker command to start the  config servers
```
docker compose -f config_server/docker-compose.yaml up -d
```
Once the instances are up, connect to the container using the below command.
```
mongosh mongodb://localhost:10001
```
Now inside the container, we have to pass the instances as members to form a replica set.
```
rs.initiate(
  {
    _id: "config_rs",
    configsvr: true,
    members: [
      { _id : 0, host : "<your-ip>:10001" },
      { _id : 1, host : "<your-ip>:10002" },
      { _id : 2, host : "<your-ip>:10003" }
    ]
  }
)
```
You can check if the replica set status using the below command.
```
rs.status()
```

### Shard servers
Repeat the same process for creating shard-1, shard-2 and shard-3 docker containers.
```
docker compose -f shard_server1/docker-compose.yaml up -d
docker compose -f shard_server2/docker-compose.yaml up -d
docker compose -f shard_server3/docker-compose.yaml up -d
```
Login into the containers:
```
mongosh mongodb://localhost:20001
mongosh mongodb://localhost:20004
mongosh mongodb://localhost:20007
```
And initiate the replica sets:
#### In shard-1:
```
rs.initiate(
  {
    _id: "shard1_rs",
    members: [
      { _id : 0, host : "<your-ip>:20001" },
      { _id : 1, host : "<your-ip>:20002" },
      { _id : 2, host : "<your-ip>:20003" }
    ]
  }
)
```

#### In shard-2:
```
rs.initiate(
  {
    _id: "shard2_rs",
    members: [
      { _id : 0, host : "<your-ip>:20004" },
      { _id : 1, host : "<your-ip>:20005" },
      { _id : 2, host : "<your-ip>:20006" }
    ]
  }
)
```

#### In shard-3:
```
rs.initiate(
  {
    _id: "shard3_rs",
    members: [
      { _id : 0, host : "<your-ip>:20007" },
      { _id : 1, host : "<your-ip>:20008" },
      { _id : 2, host : "<your-ip>:20009" }
    ]
  }
)
```

### Replica servers
Repeat the same process for creating replica-1, replica-2 and replica-3 docker containers.
```
docker compose -f replica_server1/docker-compose.yaml up -d
docker compose -f replica_server2/docker-compose.yaml up -d
docker compose -f replica_server3/docker-compose.yaml up -d
```
Login into the containers:
```
mongosh mongodb://localhost:20010
mongosh mongodb://localhost:20013
mongosh mongodb://localhost:20016
```
And initiate the replica sets:
#### In replica-1:
```
rs.initiate(
  {
    _id: "replica1_rs",
    members: [
      { _id : 0, host : "<your-ip>:20010" },
      { _id : 1, host : "<your-ip>:20011" },
      { _id : 2, host : "<your-ip>:20012" }
    ]
  }
)
```

#### In replica-2:
```
rs.initiate(
  {
    _id: "replica2_rs",
    members: [
      { _id : 0, host : "<your-ip>:20013" },
      { _id : 1, host : "<your-ip>:20014" },
      { _id : 2, host : "<your-ip>:20015" }
    ]
  }
)
```

#### In replica-3:
```
rs.initiate(
  {
    _id: "replica3_rs",
    members: [
      { _id : 0, host : "<your-ip>:20016" },
      { _id : 1, host : "<your-ip>:20017" },
      { _id : 2, host : "<your-ip>:20018" }
    ]
  }
)
```

### Mongo routers
Finally start the mongo routers:
```
docker compose -f mongo_router/docker-compose.yaml up -d
```
```
mongosh mongodb://localhost:30000
```
Inside the container, now add both shards to the cluster 
```
sh.addShard("shard1_rs/<your-ip>:20001,<your-ip>:20002,<your-ip>:20003")
sh.addShard("shard2_rs/<your-ip>:20004,<your-ip>:20005,<your-ip>:20006")
sh.addShard("shard3_rs/<your-ip>:20007,<your-ip>:20008,<your-ip>:20009")
```

**Note:** Replace ```<your-ip>``` with your IPv4 address.


### Sharding the collection
Make sure your application is always connected to mongo routers, it is not suggested to directly connect to shard replica sets.

Connect to mongo router and run this command to create a database.
```
use <database>
```

Starting in MonogDB 6.0 you don't need to run the below command to shard a collection. If you are using earlier versions then it is recommended to run it.
```
sh.enableSharding("<database>")
```

Shard your collection, this command will automatically enable sharding if your using versions Mongo 6.0 or later.
```
sh.shardCollection("<database>.<collection>", { <shard key field> : "hashed" , ... } )
```

You can check the sharding status of a database using ``sh.status()``, and data distribution across shards for a collection using: 
```db.<collection>.getShardDistribution()```
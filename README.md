## Sharding in MongoDB using docker

You can set-up sharding in MongoDB by creating a cluster of mongo instances consisting of the below components:
1. Config servers
2. Shard servers
3. Mongo routers

All the above instances are created using docker containers. In this repo we create 1 config replica set, 2 shard replica sets and 1 mongo router. Each replica set contains 3 mongo instances. 


### Pre-requisites
1. Install docker based on your platform.
2. Install mongodb from https://www.mongodb.com/docs/manual/installation/

### Starting up the mongodb network
1. Add host.docker.internal as an entry to /etc/hosts and point it to 127.0.0.1, i.e. '127.0.0.1	localhost host.docker.internal'
2. Run './docker-compose-start.sh'

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
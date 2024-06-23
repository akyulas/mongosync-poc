docker exec -it mongos1 mongosh --port 27017 --eval "sh.stopBalancer(60000, -1)"
curl localhost:27182/api/v1/start -X POST \
      --data '{
            "source": "cluster0",
            "destination": "cluster1",
            "includeNamespaces": [
                  {
                        "database": "replica_test",
                        "collections": [
                              "collection_1",
                              "collection_2",
                              "collection_3"
                        ]
                  }
            ],
            "sharding": {
                  "createSupportingIndexes": true,
                  "ignoreUnusedShardingEntries": true,
                  "shardingEntries": [
                        {
                              "database": "replica_test",
                              "collection": "collection_1",
                              "shardCollection": {
                                    "key": [
                                          {
                                                "dc": 1
                                          },
                                          {
                                                "random_id": 1
                                          }
                                    ]
                              }
                        },
                        {
                              "database": "replica_test",
                              "collection": "collection_2",
                              "shardCollection": {
                                    "key": [
                                          {
                                                "dc": 1
                                          },
                                          {
                                                "random_id": 1
                                          }
                                    ]
                              }
                        },
                        {
                              "database": "replica_test",
                              "collection": "collection_3",
                              "shardCollection": {
                                    "key": [
                                          {
                                                "dc": 1
                                          },
                                          {
                                                "random_id": 1
                                          }
                                    ]
                              }
                        }
                  ]
            }
      }'

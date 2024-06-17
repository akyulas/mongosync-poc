curl localhost:27182/api/v1/start -X POST \
      --data '{
            "source": "cluster0",
            "destination": "cluster1",
            "includeNamespaces": [
                  {
                        "database": "replica_test",
                        "collections": [ "collection_1", "collection_2", "collection_3" ]
                  }
            ]
      }'
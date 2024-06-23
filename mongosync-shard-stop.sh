curl localhost:27182/api/v1/commit -XPOST --data '{ }'
docker exec -it mongos1 mongosh --port 27017 --eval 'sh.startBalancer()'

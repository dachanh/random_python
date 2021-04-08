import redis

redis_server = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0
)



redis_server.hset("test","1","One")
redis_server.hset("test","2","Two")

print(redis_server.hkeys("test"))

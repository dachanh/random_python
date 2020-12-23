import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ""

def hello_redis():
    try:
        r = redis.StrictRedis()
        r.set("msg:hello","Hello Redis!!!")
        msg = r.get("msg:hello")
        print(msg)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    hello_redis()
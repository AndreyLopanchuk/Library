from redis.asyncio import Redis

redis_client = Redis(host="redis", port=6379, db=0)


def get_redis_client():
    return redis_client

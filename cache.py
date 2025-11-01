# app/cache.py
import os
import json
from redis import Redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis = Redis.from_url(REDIS_URL, decode_responses=True)

def get_cache(key: str):
    """Fetch a value from Redis cache."""
    value = redis.get(key)
    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value

def set_cache(key: str, value, ttl=None):
    """Set a key in cache with optional TTL."""
    data = json.dumps(value) if not isinstance(value, str) else value
    if ttl:
        redis.setex(key, ttl, data)
    else:
        redis.set(key, data)

def invalidate(key: str):
    redis.delete(key)

# Optional Pub/Sub
INVALIDATION_CHANNEL = "cache_invalidation"

def publish_invalidation(key: str):
    redis.publish(INVALIDATION_CHANNEL, key)

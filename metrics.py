# app/metrics.py
from prometheus_client import Counter, Histogram


CACHE_HIT = Counter('cache_hit_total', 'Total cache hits')
CACHE_MISS = Counter('cache_miss_total', 'Total cache misses')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency seconds')


# Use these counters in your route handlers
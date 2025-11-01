# app/routes.py
from fastapi import APIRouter, Body
from rq import Queue
from app.cache import get_cache, set_cache, invalidate, publish_invalidation, redis
from app.tasks import regenerate_product_cache
from app.metrics import CACHE_HIT, CACHE_MISS, REQUEST_LATENCY
import time

router = APIRouter()

def fetch_product_from_db(product_id: str):
    """Simulate a DB query"""
    return {"id": product_id, "name": f"DB Product {product_id}", "price": 19.99}

@router.get("/product/{product_id}")
def get_product(product_id: str):
    start = time.time()
    key = f"product:{product_id}"
    data = get_cache(key)
    if data:
        CACHE_HIT.inc()
        REQUEST_LATENCY.observe(time.time() - start)
        return {"source": "cache", "data": data}

    CACHE_MISS.inc()
    product = fetch_product_from_db(product_id)
    set_cache(key, product, ttl=300)  # 5 min
    REQUEST_LATENCY.observe(time.time() - start)
    return {"source": "db", "data": product}

@router.post("/product/{product_id}/update")
def update_product(product_id: str, payload: dict = Body(...)):
    key = f"product:{product_id}"
    db_obj = {**payload, "id": product_id}
    set_cache(key, db_obj, ttl=300)
    publish_invalidation(key)
    return {"status": "ok", "data": db_obj}

@router.post("/product/{product_id}/regenerate")
def regenerate(product_id: str):
    q = Queue(connection=redis)
    q.enqueue(regenerate_product_cache, product_id)
    return {"status": "queued"}

@router.post("/product/{product_id}/invalidate")
def invalidate_product(product_id: str):
    key = f"product:{product_id}"
    invalidate(key)
    publish_invalidation(key)
    return {"status": "invalidated"}

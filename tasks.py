# app/tasks.py
import time
from app.cache import set_cache

def regenerate_product_cache(product_id: str):
    """Background job that simulates refreshing cache."""
    time.sleep(3)  # simulate heavy DB/API work
    product = {
        "id": product_id,
        "name": f"Product {product_id}",
        "price": 9.99 + int(product_id)
    }
    key = f"product:{product_id}"
    set_cache(key, product, ttl=3600)
    return product

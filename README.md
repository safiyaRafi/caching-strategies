
# 🧠 Caching Strategies with FastAPI + Redis + RQ

This project demonstrates **practical caching strategies** in a FastAPI application using **Redis** as the cache store and **RQ (Redis Queue)** for background jobs.
It shows how to improve performance, reduce database load, and manage cache invalidation effectively.

---

## 🚀 Features

✅ **FastAPI-based REST API**
✅ **Redis caching** for performance boost
✅ **Cache invalidation** (TTL, explicit delete, versioning)
✅ **Background jobs** using **RQ Worker**
✅ **Prometheus metrics** for monitoring cache hit/miss ratios
✅ **Dockerized setup** for easy deployment

---

## 📁 Project Structure

```
caching-demo/
├── README.md
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── routes.py        # API endpoints
│   ├── cache.py         # Redis cache logic
│   ├── tasks.py         # Background job functions (RQ)
│   ├── worker_start.sh  # Script to start RQ worker
│   └── metrics.py       # Prometheus metrics setup
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/safiyaRafi/caching-strategies.git
cd caching-strategies
```

### 2️⃣ Create virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the app using Docker Compose

```bash
docker-compose up --build
```

---

## 🧩 Running Services

| Service   | Port   | Description               |
| --------- | ------ | ------------------------- |
| FastAPI   | `8000` | Web API service           |
| Redis     | `6379` | Cache & message broker    |
| RQ Worker | —      | Background task processor |

After startup:

* API runs at 👉 `http://localhost:8000`
* Swagger Docs 👉 `http://localhost:8000/docs`
* Prometheus metrics 👉 `http://localhost:8000/metrics`

---

## 🧠 Example Endpoints

### 🟢 Get Product by ID

```bash
GET /products/{product_id}
```

* Fetches product details.
* Caches result in Redis (`product:{id}` key).
* Next request is served from cache → faster response.

### 🔵 Clear Cache

```bash
DELETE /products/cache/{product_id}
```

* Explicitly invalidates a cache key.
* Useful after product updates.

---

## 🔁 Cache Strategies Implemented

| Strategy                  | Description                                  | Example                        |
| ------------------------- | -------------------------------------------- | ------------------------------ |
| **TTL (Time To Live)**    | Auto-expire cache after set time (e.g., 60s) | `SETEX product:1 60 {...}`     |
| **Explicit Invalidation** | Delete cache manually when data changes      | `DEL product:1`                |
| **Versioning**            | Use versioned keys like `product:v2:1`       | Helps after schema change      |
| **Pub/Sub (Concept)**     | Notify other services to invalidate cache    | Useful for distributed systems |
| **Write-Behind (via RQ)** | Update DB/cache in background                | Offloads heavy work to worker  |

---

## ⚙️ Background Worker (RQ)

### Start the worker:

```bash
docker exec -it caching-demo-worker-1 bash
rq worker --url redis://redis:6379
```

### Example enqueue job:

```python
from rq import Queue
from app.cache import redis as redis_client
from app.tasks import regenerate_product_cache

q = Queue(connection=redis_client)
q.enqueue(regenerate_product_cache, product_id=1)
```

---

## 📊 Monitoring

### Prometheus Metrics

Expose `/metrics` endpoint for:

* Cache hit/miss counts
* Request latency

### Redis Monitoring

```bash
docker exec -it caching-demo-redis-1 redis-cli
INFO
```

---

## 🧪 Testing Cache

```bash
# Add cache manually
SET product:1 "pen"

# Fetch cached data
GET product:1

# Delete cache
DEL product:1
```

---

## 🧰 Tech Stack

| Tool               | Purpose                       |
| ------------------ | ----------------------------- |
| **FastAPI**        | Backend Framework             |
| **Redis**          | Cache + Message Broker        |
| **RQ**             | Background Job Queue          |
| **Docker Compose** | Multi-container orchestration |
| **Prometheus**     | Metrics & Monitoring          |

---

## 📚 Learning Outcomes

✅ Understand caching benefits and trade-offs
✅ Implement Redis caching in FastAPI
✅ Manage cache invalidation (TTL, DEL, versioning)
✅ Handle background tasks using RQ workers
✅ Monitor performance with Prometheus

---

## 🧑‍💻 Author

**Safiya Rafi**
📧 [GitHub](https://github.com/safiyaRafi) | 💡 Passionate about building performant backend systems.

---


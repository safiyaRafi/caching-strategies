# app/main.py
from fastapi import FastAPI
from app.routes import router
from prometheus_client import make_asgi_app

app = FastAPI()
app.include_router(router)

# Mount Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/")
def root():
    return {"message": "Caching demo is running 🚀"}

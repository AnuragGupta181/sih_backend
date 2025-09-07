from fastapi import FastAPI
from app.routers import predict, insight, health

app = FastAPI(title="LCA Backend API", version="1.0.0")

app.include_router(predict.router)
app.include_router(insight.router)
app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "Welcome to the LCA Backend API 🚀"}

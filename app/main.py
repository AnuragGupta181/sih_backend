from fastapi import FastAPI
from app.routers import predict, insight, health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LCA Backend API", version="1.0.0")

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend URLs
    # http://localhost:8080", "https://your-frontend-domain.com
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # allow all headers
)

app.include_router(predict.router)
app.include_router(insight.router)
app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "Welcome to the LCA Backend API 🚀"}

from app.api.v1 import get_restaurants

from contextlib import asynccontextmanager
from datetime import time
from fastapi import FastAPI, APIRouter
from sqlalchemy.future import select

app = FastAPI(
    title="Restaurants Catalog API",
    description="Backend service for Restaurants Catalog (JSON API)",
    version="0.1.0",
)
api_router = APIRouter()

api_router.include_router(get_restaurants.router, prefix="/restaurants", tags=["Restaurants"])
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Restaurants Catalog API.",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }



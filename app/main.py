from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.gold import router as gold_router
from app.api.v1.auth_test import router as auth_test_router
from app.api.v1.developer import router as developer_router
from app.database.database import Base, engine
from app.scheduler.scheduler import start_scheduler

import app.models.gold_price


Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):

    start_scheduler()

    yield


app = FastAPI(
    title="Gold Intelligence API",
    description="Gold price, valuation and calculation APIs",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(auth_test_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(developer_router, prefix="/api/v1/developer", tags=["Developer"])
app.include_router(
    gold_router,
    prefix="/api/v1/gold",
    tags=["Gold"]
)


@app.get("/")
def root():

    return {
        "name": "Gold Intelligence API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

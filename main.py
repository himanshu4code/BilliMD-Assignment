from logger.blog_logger import setup_logger
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.init_db import init_database
from contextlib import asynccontextmanager
from api.blog import router as blog_router

logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database")
    init_database()
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)

# Include blog router
app.include_router(blog_router, prefix="/api", tags=["blogs"])

if __name__ == "__main__":
    logger.info("Starting application server")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

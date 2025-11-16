from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="IoT Backend",
    description="Backend para recibir datos desde Wokwi a Mongo Atlas.",
    version="1.0"
)

app.include_router(router, prefix="/api")

from fastapi import APIRouter
from datetime import datetime

from .models import SensorInput
from .db import sensor_collection

router = APIRouter()

@router.get("/")
def home():
    return {"status": "running"}

@router.post("/receive")
def receive_data(data: SensorInput):

    document = {
        "sensor_type": data.sensor_type,
        "value": data.value,
        "unit": data.unit,
        "timestamp": datetime.utcnow()
    }

    sensor_collection.insert_one(document)

    return {
        "status": "ok",
        "saved": document
    }

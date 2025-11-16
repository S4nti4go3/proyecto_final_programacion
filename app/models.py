from pydantic import BaseModel

class SensorInput(BaseModel):
    sensor_type: str
    value: float
    unit: str

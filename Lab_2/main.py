# pylint: disable=all
from datetime import datetime
from typing import List, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.ext.declarative import declared_attr
import json

from config import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
)

# SQLAlchemy setup
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Base = declarative_base()

# Define the ProcessedAgentData table
class ProcessedAgentData(Base):
    __tablename__ = "processed_agent_data"

    id = Column(Integer, primary_key=True, index=True)
    road_state = Column(String)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# FastAPI models
class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float

class GpsData(BaseModel):
    latitude: float
    longitude: float

class AgentData(BaseModel):
    accelerometer: AccelerometerData
    gps: GpsData
    timestamp: datetime

class ProcessedAgentDataInDB(BaseModel):
    id: int
    road_state: str
    x: float
    y: float
    z: float
    latitude: float
    longitude: float
    timestamp: datetime

# FastAPI app setup
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# WebSocket subscriptions
subscriptions: Set[WebSocket] = set()

# FastAPI WebSocket endpoint
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    subscriptions.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions.remove(websocket)

# Function to send data to subscribed users
async def send_data_to_subscribers(data, db):
    for websocket in subscriptions:
        await websocket.send_json(data)

# FastAPI CRUDL endpoints
@app.post("/processed_agent_data/")
async def create_processed_agent_data(data: List[ProcessedAgentDataInDB], db: Session = Depends(get_db)):
    for item in data:
        db_item = ProcessedAgentData(**item.dict())
        db.add(db_item)
    db.commit()
    await send_data_to_subscribers(data, db)
    return {"message": "Data processed successfully"}

@app.get("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def read_processed_agent_data(processed_agent_data_id: int, db: Session = Depends(get_db)):
    result = db.query(ProcessedAgentData).filter(ProcessedAgentData.id == processed_agent_data_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="ProcessedAgentData not found")
    return result

@app.get("/processed_agent_data/", response_model=List[ProcessedAgentDataInDB])
def list_processed_agent_data(db: Session = Depends(get_db)):
    return db.query(ProcessedAgentData).all()

@app.put("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentDataInDB, db: Session = Depends(get_db)):
    db_data = db.query(ProcessedAgentData).filter(ProcessedAgentData.id == processed_agent_data_id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="ProcessedAgentData not found")
    for key, value in data.dict().items():
        setattr(db_data, key, value)
    db.commit()
    return db_data

@app.delete("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def delete_processed_agent_data(processed_agent_data_id: int, db: Session = Depends(get_db)):
    db_data = db.query(ProcessedAgentData).filter(ProcessedAgentData.id == processed_agent_data_id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="ProcessedAgentData not found")
    db.delete(db_data)
    db.commit()
    return db_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

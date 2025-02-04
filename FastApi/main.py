from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import engine, SessionLocal

# Create the tables in the database (if they don't already exist).
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency - get a new database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional: Root endpoint to avoid 404 at "/"
@app.get("/")
def read_root():
    return {"message": "Welcome to the API Root!"}

# --- Detection Routes ---

@app.post("/detections/", response_model=schemas.DetectionRead)
def create_detection(detection: schemas.DetectionCreate, db: Session = Depends(get_db)):
    return crud.create_detection(db, detection)

@app.get("/detections/", response_model=List[schemas.DetectionRead])
def read_detections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    detections = crud.get_all_detections(db, skip=skip, limit=limit)
    return detections

@app.get("/detections/{detection_id}", response_model=schemas.DetectionRead)
def read_detection_by_id(detection_id: int, db: Session = Depends(get_db)):
    detection = crud.get_detection_by_id(db, detection_id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection

@app.put("/detections/{detection_id}", response_model=schemas.DetectionRead)
def update_detection_by_id(detection_id: int, detection_data: schemas.DetectionBase, db: Session = Depends(get_db)):
    updated_detection = crud.update_detection(db, detection_id, detection_data)
    if not updated_detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return updated_detection

@app.delete("/detections/{detection_id}")
def delete_detection_by_id(detection_id: int, db: Session = Depends(get_db)):
    deleted_detection = crud.delete_detection(db, detection_id)
    if not deleted_detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return {"message": "Detection deleted successfully"}

# --- Telegram Message Routes ---

@app.post("/telegram_messages/", response_model=schemas.TelegramMessageRead)
def create_telegram_message(message_data: schemas.TelegramMessageCreate, db: Session = Depends(get_db)):
    return crud.create_telegram_message(db, message_data)

@app.get("/telegram_messages/", response_model=List[schemas.TelegramMessageRead])
def read_telegram_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_all_telegram_messages(db, skip=skip, limit=limit)
    return messages

@app.get("/telegram_messages/{record_id}", response_model=schemas.TelegramMessageRead)
def read_telegram_message_by_id(record_id: int, db: Session = Depends(get_db)):
    message = crud.get_telegram_message_by_id(db, record_id)
    if not message:
        raise HTTPException(status_code=404, detail="Telegram message not found")
    return message

@app.put("/telegram_messages/{record_id}", response_model=schemas.TelegramMessageRead)
def update_telegram_message_by_id(record_id: int, update_data: schemas.TelegramMessageBase, db: Session = Depends(get_db)):
    updated_message = crud.update_telegram_message(db, record_id, update_data)
    if not updated_message:
        raise HTTPException(status_code=404, detail="Telegram message not found")
    return updated_message

@app.delete("/telegram_messages/{record_id}")
def delete_telegram_message_by_id(record_id: int, db: Session = Depends(get_db)):
    deleted_message = crud.delete_telegram_message(db, record_id)
    if not deleted_message:
        raise HTTPException(status_code=404, detail="Telegram message not found")
    return {"message": "Telegram message deleted successfully"}

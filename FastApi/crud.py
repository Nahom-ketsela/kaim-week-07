from sqlalchemy.orm import Session
from . import models, schemas

#
# CRUD for Detection
#
def create_detection(db: Session, detection_data: schemas.DetectionCreate):
    detection = models.Detection(**detection_data.dict())
    db.add(detection)
    db.commit()
    db.refresh(detection)
    return detection

def get_detection_by_id(db: Session, detection_id: int):
    return db.query(models.Detection).filter(models.Detection.id == detection_id).first()

def get_all_detections(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Detection).offset(skip).limit(limit).all()

def update_detection(db: Session, detection_id: int, detection_data: schemas.DetectionBase):
    detection = get_detection_by_id(db, detection_id)
    if detection:
        for field, value in detection_data.dict(exclude_unset=True).items():
            setattr(detection, field, value)
        db.commit()
        db.refresh(detection)
    return detection

def delete_detection(db: Session, detection_id: int):
    detection = get_detection_by_id(db, detection_id)
    if detection:
        db.delete(detection)
        db.commit()
    return detection


#
# CRUD for TelegramMessage
#
def create_telegram_message(db: Session, message_data: schemas.TelegramMessageCreate):
    message = models.TelegramMessage(**message_data.dict())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_telegram_message_by_id(db: Session, message_id: int):
    return db.query(models.TelegramMessage).filter(models.TelegramMessage.id == message_id).first()

def get_all_telegram_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TelegramMessage).offset(skip).limit(limit).all()

def update_telegram_message(db: Session, record_id: int, update_data: schemas.TelegramMessageBase):
    message = get_telegram_message_by_id(db, record_id)
    if message:
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(message, field, value)
        db.commit()
        db.refresh(message)
    return message

def delete_telegram_message(db: Session, record_id: int):
    message = get_telegram_message_by_id(db, record_id)
    if message:
        db.delete(message)
        db.commit()
    return message

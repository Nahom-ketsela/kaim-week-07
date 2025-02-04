from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Detections
class DetectionBase(BaseModel):
    image_name: Optional[str] = None
    class_id: Optional[int] = None
    x_center: Optional[float] = None
    y_center: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    confidence: Optional[float] = None

class DetectionCreate(DetectionBase):
    pass

class DetectionRead(DetectionBase):
    id: int

    # Pydantic v2 style
    model_config = ConfigDict(from_attributes=True)

# Telegram Messages
class TelegramMessageBase(BaseModel):
    channel_username: Optional[str] = None
    sender_id: Optional[int] = None
    message_id: Optional[int] = None
    message: Optional[str] = None
    message_date: Optional[datetime] = None
    media_path: Optional[str] = None
    emoji_used: Optional[str] = None
    youtube_links: Optional[str] = None

class TelegramMessageCreate(TelegramMessageBase):
    pass

class TelegramMessageRead(TelegramMessageBase):
    id: int

    # Pydantic v2 style
    model_config = ConfigDict(from_attributes=True)

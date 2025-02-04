from sqlalchemy import Column, Integer, Text, BigInteger, Double, TIMESTAMP
from sqlalchemy import String
from .database import Base

# If "Double" isn't recognized, replace the import above with:
# from sqlalchemy import Float as Double

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(Text, nullable=True)
    class_id = Column(Integer, nullable=True)
    x_center = Column(Double, nullable=True)
    y_center = Column(Double, nullable=True)
    width = Column(Double, nullable=True)
    height = Column(Double, nullable=True)
    confidence = Column(Double, nullable=True)


class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    id = Column(Integer, primary_key=True, index=True)
    channel_username = Column(Text, nullable=True)
    sender_id = Column(BigInteger, nullable=True)
    message_id = Column(BigInteger, unique=True, nullable=True)
    message = Column(Text, nullable=True)
    message_date = Column(TIMESTAMP, nullable=True)
    media_path = Column(Text, nullable=True)
    emoji_used = Column(Text, nullable=True)
    youtube_links = Column(Text, nullable=True)

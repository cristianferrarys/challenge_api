import uuid

from pydantic import BaseModel, ConfigDict, Field
from app.enums.notification_channel import NotificationChannel

class NotiCreate(BaseModel):
    titulo: str = Field(min_length=2, max_length=100)
    contenido: str = Field(min_length=2, max_length=200)
    canal: NotificationChannel
    destinatario: str = Field(min_length=2, max_length=100)


class NotiUpdate(BaseModel):
    titulo: str = Field(min_length=2, max_length=100)
    contenido: str = Field(min_length=2, max_length=200)
    canal: str = Field(min_length=6, max_length=200)


class NotiResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    titulo: str
    contenido: str
    canal: str
    destinatario: str
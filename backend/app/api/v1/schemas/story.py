import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import Priority, Status


class StoryBase(BaseModel):
    title: str
    description: str | None = None
    priority: Priority = Priority.MID


class StoryCreate(StoryBase):
    pass


class StoryUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None


class StoryRead(StoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    charter_id: uuid.UUID
    status: Status
    created_at: datetime
    updated_at: datetime

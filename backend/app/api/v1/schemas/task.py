import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import Priority, Status


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    priority: Priority = Priority.MID
    due_date: date | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    due_date: date | None = None


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    story_id: uuid.UUID
    status: Status
    created_at: datetime
    updated_at: datetime

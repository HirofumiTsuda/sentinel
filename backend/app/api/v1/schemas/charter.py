import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import Status


class CharterBase(BaseModel):
    title: str
    description: str | None = None


class CharterCreate(CharterBase):
    pass


class CharterUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None


class CharterRead(CharterBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    status: Status
    created_at: datetime
    updated_at: datetime

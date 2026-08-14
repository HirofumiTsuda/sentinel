import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import Status


class ProjectBase(BaseModel):
    title: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: Status
    created_at: datetime
    updated_at: datetime

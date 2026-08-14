import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import Priority, priority_enum
from app.models.mixins import CommonFieldsMixin


class Task(CommonFieldsMixin, Base):
    """A unit of work that realizes a story. Belongs to exactly one
    story; never spans multiple stories."""

    __tablename__ = "tasks"

    story_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("stories.id", ondelete="CASCADE"), nullable=False
    )
    priority: Mapped[Priority] = mapped_column(
        priority_enum, nullable=False, default=Priority.MID
    )
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import Priority, priority_enum
from app.models.mixins import CommonFieldsMixin


class Story(CommonFieldsMixin, Base):
    """A concrete effort toward achieving a charter. Belongs to exactly
    one charter; never spans multiple charters."""

    __tablename__ = "stories"

    charter_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("charters.id", ondelete="CASCADE"), nullable=False
    )
    priority: Mapped[Priority] = mapped_column(
        priority_enum, nullable=False, default=Priority.MID
    )

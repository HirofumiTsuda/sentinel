import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import CommonFieldsMixin


class Charter(CommonFieldsMixin, Base):
    """States the purpose/direction of a project. A project can have
    multiple charters; description holds the vision/purpose itself."""

    __tablename__ = "charters"

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )

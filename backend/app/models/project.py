from app.db.base import Base
from app.models.mixins import CommonFieldsMixin


class Project(CommonFieldsMixin, Base):
    """Top-level container. A project can hold multiple charters.
    Single-user app: no owner/user reference needed."""

    __tablename__ = "projects"

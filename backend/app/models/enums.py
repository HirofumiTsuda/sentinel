import enum

from sqlalchemy import Enum


class Status(enum.StrEnum):
    """Common status shared across every level of the hierarchy
    (project / charter / story / task)."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(enum.StrEnum):
    """Priority used by stories and tasks."""

    HIGH = "high"
    MID = "mid"
    LOW = "low"


# Shared instances: reusing the same object across columns/tables means
# SQLAlchemy creates a single Postgres ENUM type ("status" / "priority")
# instead of one per table.
status_enum = Enum(Status, name="status")
priority_enum = Enum(Priority, name="priority")

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Common base class for all models. Alembic autogenerate reads this metadata."""

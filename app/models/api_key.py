from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone

from app.database.database import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    key_prefix = Column(
        String,
        nullable=False,
        index=True
    )

    key_hash = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )

    active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    request_count = Column(
        Integer,
        default=0,
        nullable=False
    )

    plan = Column(
        String,
        default="free",
        nullable=False
    )

    monthly_limit = Column(
        Integer,
        default=1000,
        nullable=False
    )

    last_used_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    revoked_at = Column(
        DateTime,
        nullable=True
    )

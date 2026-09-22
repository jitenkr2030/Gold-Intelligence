from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone

from app.database.database import Base


class GoldWebhook(Base):
    __tablename__ = "gold_webhooks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    url = Column(
        String,
        nullable=False
    )

    event = Column(
        String,
        default="gold_alert_triggered",
        nullable=False
    )

    active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

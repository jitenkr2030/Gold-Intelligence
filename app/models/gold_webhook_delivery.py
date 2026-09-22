from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime, timezone

from app.database.database import Base


class GoldWebhookDelivery(Base):
    __tablename__ = "gold_webhook_deliveries"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    webhook_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    alert_id = Column(
        Integer,
        nullable=True,
        index=True
    )

    event = Column(
        String,
        nullable=False
    )

    payload = Column(
        Text,
        nullable=False
    )

    status_code = Column(
        Integer,
        nullable=True
    )

    success = Column(
        Boolean,
        default=False,
        nullable=False
    )

    error = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

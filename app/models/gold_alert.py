from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from datetime import datetime, timezone

from app.database.database import Base


class GoldAlert(Base):
    __tablename__ = "gold_alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    purity = Column(
        Integer,
        nullable=False
    )

    target_price = Column(
        Float,
        nullable=False
    )

    condition = Column(
        String,
        nullable=False
    )

    currency = Column(
        String,
        default="INR",
        nullable=False
    )

    unit = Column(
        String,
        default="gram",
        nullable=False
    )

    active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    triggered = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    triggered_at = Column(
        DateTime,
        nullable=True
    )

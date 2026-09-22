from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime, timezone
from app.database.database import Base


class GoldPrice(Base):
    __tablename__ = "gold_prices"

    id = Column(Integer, primary_key=True, index=True)

    metal = Column(
        String,
        default="gold",
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

    price_24k = Column(
        Float,
        nullable=False
    )

    price_22k = Column(
        Float,
        nullable=False
    )

    price_18k = Column(
        Float,
        nullable=False
    )

    source = Column(
        String,
        nullable=False
    )

    provider_timestamp = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

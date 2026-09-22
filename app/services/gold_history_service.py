from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.gold_price import GoldPrice


class GoldHistoryService:

    def get_history(
        self,
        db: Session,
        days: int = 7
    ):
        if days < 1:
            days = 1

        if days > 365:
            days = 365

        now = datetime.now(timezone.utc)
        start_date = now - timedelta(days=days)

        records = (
            db.query(GoldPrice)
            .filter(GoldPrice.created_at >= start_date)
            .order_by(GoldPrice.created_at.asc())
            .all()
        )

        return records

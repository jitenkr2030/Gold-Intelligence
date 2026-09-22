from app.database.database import SessionLocal
from app.services.gold_price_service import GoldPriceService


class GoldPriceCollector:

    def __init__(self):
        self.service = GoldPriceService()

    def collect(self):

        db = SessionLocal()

        try:
            price = self.service.get_current_price(db)

            return {
                "success": True,
                "id": price.id,
                "source": price.source,
                "price_24k": price.price_24k,
                "price_22k": price.price_22k,
                "price_18k": price.price_18k,
                "timestamp": price.created_at
            }

        finally:
            db.close()

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.gold_price import GoldPrice
from app.providers.gold_price_provider import GoldPriceProvider


class GoldPriceService:

    def __init__(self):
        self.provider = GoldPriceProvider()

    def fetch_current_price(self):
        """
        Fetch latest gold price from external provider.
        Does NOT save anything to database.
        """

        return self.provider.get_current_price()

    def save_price(self, db: Session, price_data: dict):
        """
        Save a fetched gold price snapshot to database.
        """

        provider_timestamp = None

        if price_data.get("provider_timestamp"):
            provider_timestamp = datetime.fromisoformat(
                price_data["provider_timestamp"].replace("Z", "+00:00")
            )

        price = GoldPrice(
            metal=price_data["metal"],
            currency=price_data["currency"],
            unit=price_data["unit"],
            price_24k=price_data["price_24k"],
            price_22k=price_data["price_22k"],
            price_18k=price_data["price_18k"],
            source=price_data["source"],
            provider_timestamp=provider_timestamp
        )

        db.add(price)
        db.commit()
        db.refresh(price)

        return price

    def get_current_price(self, db: Session):
        """
        Backward-compatible method:
        Fetch price and save it.
        Used by collector.
        """

        price_data = self.fetch_current_price()

        return self.save_price(
            db=db,
            price_data=price_data
        )

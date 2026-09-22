from app.database.database import SessionLocal

from app.models.gold_alert import GoldAlert
from app.models.gold_webhook import GoldWebhook

from app.services.gold_price_service import GoldPriceService
from app.services.gold_alert_service import GoldAlertService
from app.services.gold_webhook_service import GoldWebhookService


class GoldAlertChecker:

    def __init__(self):

        self.price_service = GoldPriceService()
        self.alert_service = GoldAlertService()
        self.webhook_service = GoldWebhookService()

    def check_alerts(self):

        db = SessionLocal()

        try:

            price_data = (
                self.price_service.fetch_current_price()
            )

            prices = {
                24: price_data["price_24k"],
                22: price_data["price_22k"],
                18: price_data["price_18k"]
            }

            alerts = (
                db.query(GoldAlert)
                .filter(
                    GoldAlert.active == True,
                    GoldAlert.triggered == False
                )
                .all()
            )

            webhooks = (
                db.query(GoldWebhook)
                .filter(
                    GoldWebhook.active == True,
                    GoldWebhook.event == "gold_alert_triggered"
                )
                .all()
            )

            results = []

            for alert in alerts:

                current_price = prices.get(
                    alert.purity
                )

                if current_price is None:
                    continue

                triggered = self.alert_service.check_alert(
                    db=db,
                    alert=alert,
                    current_price=current_price
                )

                webhook_results = []

                if triggered:

                    payload = {
                        "event": "gold_alert_triggered",
                        "alert_id": alert.id,
                        "purity": f"{alert.purity}K",
                        "current_price": current_price,
                        "target_price": alert.target_price,
                        "condition": alert.condition,
                        "currency": alert.currency,
                        "unit": alert.unit
                    }

                    for webhook in webhooks:

                        webhook_result = (
                            self.webhook_service.send_webhook(
                                db=db,
                                webhook=webhook,
                                payload=payload
                            )
                        )

                        webhook_results.append({
                            "webhook_id": webhook.id,
                            **webhook_result
                        })

                results.append({
                    "alert_id": alert.id,
                    "purity": f"{alert.purity}K",
                    "current_price": current_price,
                    "target_price": alert.target_price,
                    "condition": alert.condition,
                    "triggered": triggered,
                    "webhooks": webhook_results
                })

            return {
                "success": True,
                "checked": len(results),
                "results": results
            }

        finally:

            db.close()

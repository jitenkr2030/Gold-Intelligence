import json
import requests

from sqlalchemy.orm import Session

from app.models.gold_webhook import GoldWebhook
from app.models.gold_webhook_delivery import GoldWebhookDelivery


class GoldWebhookService:

    def create_webhook(
        self,
        db: Session,
        url: str,
        event: str = "gold_alert_triggered"
    ):

        webhook = GoldWebhook(
            url=url,
            event=event,
            active=True
        )

        db.add(webhook)
        db.commit()
        db.refresh(webhook)

        return webhook

    def get_webhooks(
        self,
        db: Session
    ):

        return (
            db.query(GoldWebhook)
            .order_by(GoldWebhook.created_at.desc())
            .all()
        )

    def deactivate_webhook(
        self,
        db: Session,
        webhook_id: int
    ):

        webhook = (
            db.query(GoldWebhook)
            .filter(GoldWebhook.id == webhook_id)
            .first()
        )

        if not webhook:
            return None

        webhook.active = False

        db.commit()
        db.refresh(webhook)

        return webhook

    def send_webhook(
        self,
        db: Session,
        webhook: GoldWebhook,
        payload: dict
    ):

        if not webhook.active:

            delivery = GoldWebhookDelivery(
                webhook_id=webhook.id,
                alert_id=payload.get("alert_id"),
                event=payload.get(
                    "event",
                    webhook.event
                ),
                payload=json.dumps(payload),
                status_code=None,
                success=False,
                error="Webhook is inactive"
            )

            db.add(delivery)
            db.commit()

            return {
                "success": False,
                "reason": "Webhook is inactive"
            }

        try:

            response = requests.post(
                webhook.url,
                json=payload,
                timeout=10
            )

            delivery = GoldWebhookDelivery(
                webhook_id=webhook.id,
                alert_id=payload.get("alert_id"),
                event=payload.get(
                    "event",
                    webhook.event
                ),
                payload=json.dumps(payload),
                status_code=response.status_code,
                success=response.ok,
                error=None
            )

            db.add(delivery)
            db.commit()

            return {
                "success": response.ok,
                "status_code": response.status_code
            }

        except requests.RequestException as error:

            delivery = GoldWebhookDelivery(
                webhook_id=webhook.id,
                alert_id=payload.get("alert_id"),
                event=payload.get(
                    "event",
                    webhook.event
                ),
                payload=json.dumps(payload),
                status_code=None,
                success=False,
                error=str(error)
            )

            db.add(delivery)
            db.commit()

            return {
                "success": False,
                "error": str(error)
            }


    def get_delivery_history(
        self,
        db: Session
    ):

        return (
            db.query(GoldWebhookDelivery)
            .order_by(
                GoldWebhookDelivery.created_at.desc()
            )
            .all()
        )

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.gold_alert import GoldAlert


class GoldAlertService:

    SUPPORTED_PURITIES = {24, 22, 18}
    SUPPORTED_CONDITIONS = {"above", "below"}

    def create_alert(
        self,
        db: Session,
        purity: int,
        target_price: float,
        condition: str,
        currency: str = "INR",
        unit: str = "gram"
    ):

        if purity not in self.SUPPORTED_PURITIES:
            raise ValueError(
                "Unsupported purity. Use 24K, 22K or 18K."
            )

        condition = condition.lower().strip()

        if condition not in self.SUPPORTED_CONDITIONS:
            raise ValueError(
                "Unsupported condition. Use 'above' or 'below'."
            )

        alert = GoldAlert(
            purity=purity,
            target_price=target_price,
            condition=condition,
            currency=currency,
            unit=unit,
            active=True,
            triggered=False
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        return alert

    def get_alert(
        self,
        db: Session,
        alert_id: int
    ):

        return (
            db.query(GoldAlert)
            .filter(GoldAlert.id == alert_id)
            .first()
        )

    def deactivate_alert(
        self,
        db: Session,
        alert_id: int
    ):

        alert = self.get_alert(
            db=db,
            alert_id=alert_id
        )

        if not alert:
            return None

        alert.active = False

        db.commit()
        db.refresh(alert)

        return alert

    def check_alert(
        self,
        db: Session,
        alert: GoldAlert,
        current_price: float
    ):

        if not alert.active or alert.triggered:
            return False

        triggered = False

        if alert.condition == "above":
            triggered = current_price >= alert.target_price

        elif alert.condition == "below":
            triggered = current_price <= alert.target_price

        if triggered:
            alert.triggered = True
            alert.triggered_at = datetime.now(timezone.utc)

            db.commit()
            db.refresh(alert)

            return True

        return False

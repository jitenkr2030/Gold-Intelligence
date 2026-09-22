from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.gold_price_service import GoldPriceService
from app.services.gold_history_service import GoldHistoryService

from app.schemas.gold_calculator import GoldCalculationRequest
from app.services.gold_calculator_service import GoldCalculatorService

from app.schemas.jewellery_calculator import JewelleryCalculationRequest
from app.services.jewellery_calculator_service import JewelleryCalculatorService

from app.schemas.purity_calculator import PurityCalculationRequest
from app.services.purity_calculator_service import PurityCalculatorService

from app.schemas.buyback_calculator import BuybackCalculationRequest
from app.services.buyback_calculator_service import BuybackCalculatorService

from app.schemas.gold_loan_calculator import GoldLoanCalculationRequest
from app.services.gold_loan_calculator_service import GoldLoanCalculatorService

from app.schemas.gold_alert import GoldAlertCreateRequest
from app.services.gold_alert_service import GoldAlertService
from app.models.gold_alert import GoldAlert

from app.schemas.gold_webhook import GoldWebhookCreateRequest
from app.services.gold_webhook_service import GoldWebhookService
from app.schemas.api_key import APIKeyCreateRequest
from app.services.api_key_service import APIKeyService
from app.api.dependencies import require_api_key
from app.models.api_key import APIKey





router = APIRouter()

gold_service = GoldPriceService()
history_service = GoldHistoryService()
calculator_service = GoldCalculatorService()
jewellery_calculator_service = JewelleryCalculatorService()
purity_calculator_service = PurityCalculatorService()
buyback_calculator_service = BuybackCalculatorService()
gold_loan_calculator_service = GoldLoanCalculatorService()
gold_alert_service = GoldAlertService()


@router.get("/price")
def get_gold_price(
    api_key: APIKey = Depends(require_api_key)
):

    price = gold_service.fetch_current_price()

    return {
        "success": True,
        "data": {
            "metal": price["metal"],
            "currency": price["currency"],
            "unit": price["unit"],
            "purity": {
                "24K": price["price_24k"],
                "22K": price["price_22k"],
                "18K": price["price_18k"]
            },
            "source": price["source"],
            "provider_timestamp": price["provider_timestamp"]
        }
    }


@router.get("/history")
def get_gold_history(
    days: int = Query(
        default=7,
        ge=1,
        le=365,
        description="Number of previous days"
    ),
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(require_api_key)
):

    records = history_service.get_history(
        db=db,
        days=days
    )

    data = []

    for record in records:
        data.append({
            "id": record.id,
            "timestamp": record.created_at,
            "provider_timestamp": record.provider_timestamp,
            "24K": record.price_24k,
            "22K": record.price_22k,
            "18K": record.price_18k,
            "currency": record.currency,
            "unit": record.unit,
            "source": record.source
        })

    return {
        "success": True,
        "period": {
            "days": days
        },
        "count": len(data),
        "data": data
    }


@router.post("/calculate")
def calculate_gold(
    request: GoldCalculationRequest,
    api_key: APIKey = Depends(require_api_key)
):

    try:

        price_data = gold_service.fetch_current_price()

        result = calculator_service.calculate(
            purity=request.purity,
            weight_grams=request.weight_grams,
            price_data=price_data
        )

        return {
            "success": True,
            "data": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/jewellery/calculate")
def calculate_jewellery(
    request: JewelleryCalculationRequest,
    api_key: APIKey = Depends(require_api_key)
):

    try:

        price_data = gold_service.fetch_current_price()

        result = jewellery_calculator_service.calculate(
            purity=request.purity,
            weight_grams=request.weight_grams,
            wastage_percent=request.wastage_percent,
            making_charge_percent=request.making_charge_percent,
            gst_percent=request.gst_percent,
            price_data=price_data
        )

        return {
            "success": True,
            "data": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/purity/calculate")
def calculate_purity(
    request: PurityCalculationRequest,
    api_key: APIKey = Depends(require_api_key)
):

    try:

        result = purity_calculator_service.calculate(
            purity=request.purity,
            weight_grams=request.weight_grams
        )

        return {
            "success": True,
            "data": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/buyback/calculate")
def calculate_buyback(
    request: BuybackCalculationRequest,
    api_key: APIKey = Depends(require_api_key)
):

    try:

        price_data = gold_service.fetch_current_price()

        result = buyback_calculator_service.calculate(
            purity=request.purity,
            weight_grams=request.weight_grams,
            buyback_discount_percent=request.buyback_discount_percent,
            price_data=price_data
        )

        return {
            "success": True,
            "data": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/loan/calculate")
def calculate_gold_loan(
    request: GoldLoanCalculationRequest,
    api_key: APIKey = Depends(require_api_key)
):

    try:

        price_data = gold_service.fetch_current_price()

        result = gold_loan_calculator_service.calculate(
            purity=request.purity,
            weight_grams=request.weight_grams,
            loan_to_value_percent=request.loan_to_value_percent,
            interest_rate_percent=request.interest_rate_percent,
            tenure_months=request.tenure_months,
            price_data=price_data
        )

        return {
            "success": True,
            "data": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/alerts")
def create_gold_alert(
    request: GoldAlertCreateRequest,
    db: Session = Depends(get_db)
):

    try:

        alert = gold_alert_service.create_alert(
            db=db,
            purity=request.purity,
            target_price=request.target_price,
            condition=request.condition,
            currency=request.currency,
            unit=request.unit
        )

        return {
            "success": True,
            "message": "Gold price alert created successfully.",
            "data": {
                "id": alert.id,
                "purity": f"{alert.purity}K",
                "target_price": alert.target_price,
                "condition": alert.condition,
                "currency": alert.currency,
                "unit": alert.unit,
                "active": alert.active,
                "triggered": alert.triggered,
                "created_at": alert.created_at
            }
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get("/alerts")
def get_gold_alerts(
    db: Session = Depends(get_db)
):

    alerts = (
        db.query(GoldAlert)
        .order_by(GoldAlert.created_at.desc())
        .all()
    )

    data = []

    for alert in alerts:
        data.append({
            "id": alert.id,
            "purity": f"{alert.purity}K",
            "target_price": alert.target_price,
            "condition": alert.condition,
            "currency": alert.currency,
            "unit": alert.unit,
            "active": alert.active,
            "triggered": alert.triggered,
            "created_at": alert.created_at,
            "triggered_at": alert.triggered_at
        })

    return {
        "success": True,
        "count": len(data),
        "data": data
    }


@router.patch("/alerts/{alert_id}/deactivate")
def deactivate_gold_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = gold_alert_service.deactivate_alert(
        db=db,
        alert_id=alert_id
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Gold alert not found."
        )

    return {
        "success": True,
        "message": "Gold price alert deactivated.",
        "data": {
            "id": alert.id,
            "purity": f"{alert.purity}K",
            "target_price": alert.target_price,
            "condition": alert.condition,
            "active": alert.active,
            "triggered": alert.triggered
        }
    }



gold_webhook_service = GoldWebhookService()
api_key_service = APIKeyService()

@router.post("/webhooks")
def create_gold_webhook(
    request: GoldWebhookCreateRequest,
    db: Session = Depends(get_db)
):

    webhook = gold_webhook_service.create_webhook(
        db=db,
        url=request.url,
        event=request.event
    )

    return {
        "success": True,
        "message": "Gold webhook created successfully.",
        "data": {
            "id": webhook.id,
            "url": webhook.url,
            "event": webhook.event,
            "active": webhook.active,
            "created_at": webhook.created_at
        }
    }


@router.get("/webhooks")
def get_gold_webhooks(
    db: Session = Depends(get_db)
):

    webhooks = gold_webhook_service.get_webhooks(
        db=db
    )

    data = []

    for webhook in webhooks:

        data.append({
            "id": webhook.id,
            "url": webhook.url,
            "event": webhook.event,
            "active": webhook.active,
            "created_at": webhook.created_at
        })

    return {
        "success": True,
        "count": len(data),
        "data": data
    }


@router.patch("/webhooks/{webhook_id}/deactivate")
def deactivate_gold_webhook(
    webhook_id: int,
    db: Session = Depends(get_db)
):

    webhook = gold_webhook_service.deactivate_webhook(
        db=db,
        webhook_id=webhook_id
    )

    if not webhook:

        raise HTTPException(
            status_code=404,
            detail="Gold webhook not found."
        )

    return {
        "success": True,
        "message": "Gold webhook deactivated.",
        "data": {
            "id": webhook.id,
            "url": webhook.url,
            "event": webhook.event,
            "active": webhook.active
        }
    }


@router.get("/webhooks/deliveries")
def get_gold_webhook_deliveries(
    db: Session = Depends(get_db)
):

    deliveries = (
        gold_webhook_service.get_delivery_history(
            db=db
        )
    )

    data = []

    for delivery in deliveries:

        data.append({
            "id": delivery.id,
            "webhook_id": delivery.webhook_id,
            "alert_id": delivery.alert_id,
            "event": delivery.event,
            "status_code": delivery.status_code,
            "success": delivery.success,
            "error": delivery.error,
            "created_at": delivery.created_at
        })

    return {
        "success": True,
        "count": len(data),
        "data": data
    }


@router.post("/keys")
def create_api_key(
    request: APIKeyCreateRequest,
    db: Session = Depends(get_db)
):

    result = api_key_service.create_key(
        db=db,
        name=request.name,
        plan=request.plan
    )

    return {
        "success": True,
        "message": "API key created successfully. Store this key securely; it will not be shown again.",
        "data": result
    }


@router.get("/keys")
def get_api_keys(
    db: Session = Depends(get_db)
):
    keys = api_key_service.get_keys(db=db)

    data = []

    for key in keys:
        data.append({
            "id": key.id,
            "name": key.name,
            "key_prefix": key.key_prefix,
            "active": key.active,
            "request_count": key.request_count,
            "plan": key.plan,
            "monthly_limit": key.monthly_limit,
            "usage_remaining": max(
                0,
                key.monthly_limit - key.request_count
            ),
            "last_used_at": key.last_used_at,
            "created_at": key.created_at,
            "revoked_at": key.revoked_at
        })

    return {
        "success": True,
        "count": len(data),
        "data": data
    }


@router.patch("/keys/{key_id}/revoke")
def revoke_api_key(
    key_id: int,
    db: Session = Depends(get_db)
):
    key = api_key_service.revoke_key(
        db=db,
        key_id=key_id
    )

    if not key:
        raise HTTPException(
            status_code=404,
            detail="API key not found."
        )

    return {
        "success": True,
        "message": "API key revoked successfully.",
        "data": {
            "id": key.id,
            "name": key.name,
            "key_prefix": key.key_prefix,
            "active": key.active,
            "revoked_at": key.revoked_at
        }
    }

# ============================================================
# Indian Jewellery Pricing V2
# ============================================================

from app.schemas.jewellery_v2 import JewelleryPricingV2Request
from app.services.jewellery_v2_service import JewelleryPricingV2Service

jewellery_v2_service = JewelleryPricingV2Service()


@router.post(
    "/jewellery/v2/calculate",
    summary="Indian Jewellery Pricing V2",
    description=(
        "Calculate jewellery price using gold purity, gross weight, "
        "stone weight, wastage, making charges, stone charges, "
        "discount and GST."
    )
)
def calculate_jewellery_v2(
    request: JewelleryPricingV2Request,
    api_key: APIKey = Depends(require_api_key)
):
    try:
        price_data = gold_service.fetch_current_price()

        result = jewellery_v2_service.calculate(
            request=request,
            price_data=price_data
        )

        return {
            "success": True,
            "data": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.api_key_service import APIKeyService
from app.security.rate_limiter import rate_limiter

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)

api_key_service = APIKeyService()


def require_api_key(
    x_api_key: str = Depends(api_key_header),
    db: Session = Depends(get_db)
):
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is required."
        )

    api_key = api_key_service.verify_key(
        db=db,
        raw_key=x_api_key
    )

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive API key."
        )

    # Monthly usage limit
    if api_key.request_count > api_key.monthly_limit:
        raise HTTPException(
            status_code=429,
            detail={
                "message": "Monthly API usage limit exceeded.",
                "plan": api_key.plan,
                "monthly_limit": api_key.monthly_limit,
                "request_count": api_key.request_count
            }
        )

    # Per-minute rate limit
    if not rate_limiter.check(api_key.id):
        raise HTTPException(
            status_code=429,
            detail={
                "message": "Rate limit exceeded.",
                "limit": "60 requests per minute"
            }
        )

    return api_key

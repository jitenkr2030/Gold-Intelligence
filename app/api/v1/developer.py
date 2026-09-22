from fastapi import APIRouter, Depends

from app.api.dependencies import require_api_key
from app.models.api_key import APIKey


router = APIRouter()


@router.get("/dashboard")
def developer_dashboard(
    api_key: APIKey = Depends(require_api_key)
):
    return {
        "success": True,
        "data": {
            "api_key": {
                "id": api_key.id,
                "name": api_key.name,
                "prefix": api_key.key_prefix,
                "active": api_key.active
            },
            "plan": {
                "name": api_key.plan,
                "monthly_limit": api_key.monthly_limit
            },
            "usage": {
                "requests_used": api_key.request_count,
                "requests_remaining": max(
                    0,
                    api_key.monthly_limit - api_key.request_count
                ),
                "usage_percent": round(
                    (
                        api_key.request_count
                        / api_key.monthly_limit
                    ) * 100,
                    2
                ) if api_key.monthly_limit else 0
            },
            "last_used_at": api_key.last_used_at,
            "created_at": api_key.created_at,
            "revoked_at": api_key.revoked_at
        }
    }

from fastapi import APIRouter, Depends

from app.api.dependencies import require_api_key
from app.models.api_key import APIKey


router = APIRouter()


@router.get("/protected-test")
def protected_test(
    api_key: APIKey = Depends(require_api_key)
):

    return {
        "success": True,
        "message": "API key authentication successful.",
        "data": {
            "key_id": api_key.id,
            "key_name": api_key.name,
            "request_count": api_key.request_count,
            "last_used_at": api_key.last_used_at
        }
    }

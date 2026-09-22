import hashlib
import secrets

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.api_key import APIKey


class APIKeyService:

    KEY_PREFIX = "gi_live_"

    PLANS = {
        "free": 1000,
        "developer": 10000,
        "business": 100000
    }

    def generate_key(self):

        random_part = secrets.token_urlsafe(32)

        return self.KEY_PREFIX + random_part

    def hash_key(self, raw_key: str):

        return hashlib.sha256(
            raw_key.encode("utf-8")
        ).hexdigest()

    def create_key(
        self,
        db: Session,
        name: str,
        plan: str = "free"
    ):

        plan = plan.lower().strip()

        if plan not in self.PLANS:
            raise ValueError(
                "Invalid plan. Use free, developer or business."
            )

        raw_key = self.generate_key()

        key_hash = self.hash_key(raw_key)

        key_prefix = raw_key[:16]

        api_key = APIKey(
            name=name,
            key_prefix=key_prefix,
            key_hash=key_hash,
            active=True,
            request_count=0,
            plan=plan,
            monthly_limit=self.PLANS[plan]
        )

        db.add(api_key)

        db.commit()

        db.refresh(api_key)

        return {
            "id": api_key.id,
            "name": api_key.name,
            "api_key": raw_key,
            "key_prefix": api_key.key_prefix,
            "plan": api_key.plan,
            "monthly_limit": api_key.monthly_limit,
            "active": api_key.active,
            "created_at": api_key.created_at
        }

    def verify_key(
        self,
        db: Session,
        raw_key: str
    ):

        key_hash = self.hash_key(raw_key)

        api_key = (
            db.query(APIKey)
            .filter(
                APIKey.key_hash == key_hash,
                APIKey.active == True
            )
            .first()
        )

        if not api_key:
            return None

        api_key.request_count += 1

        api_key.last_used_at = datetime.now(timezone.utc)

        db.commit()

        db.refresh(api_key)

        return api_key

    def get_keys(self, db: Session):

        return (
            db.query(APIKey)
            .order_by(APIKey.created_at.desc())
            .all()
        )

    def revoke_key(
        self,
        db: Session,
        key_id: int
    ):

        api_key = (
            db.query(APIKey)
            .filter(APIKey.id == key_id)
            .first()
        )

        if not api_key:
            return None

        if api_key.active:

            api_key.active = False

            api_key.revoked_at = datetime.now(timezone.utc)

            db.commit()

            db.refresh(api_key)

        return api_key

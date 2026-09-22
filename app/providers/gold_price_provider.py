import requests
from app.config import METALS_DEV_API_KEY, METALS_DEV_BASE_URL


class GoldPriceProvider:

    def get_current_price(self):

        if not METALS_DEV_API_KEY:
            raise RuntimeError(
                "METALS_DEV_API_KEY is not configured"
            )

        url = f"{METALS_DEV_BASE_URL}/latest"

        params = {
            "api_key": METALS_DEV_API_KEY,
            "currency": "INR",
            "unit": "g"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        if result.get("status") != "success":
            raise RuntimeError(
                f"Gold provider error: {result}"
            )

        gold_price = result["metals"]["gold"]

        price_24k = float(gold_price)
        price_22k = price_24k * (22 / 24)
        price_18k = price_24k * (18 / 24)

        provider_timestamp = (
            result.get("timestamps", {})
            .get("metal")
        )

        return {
            "metal": "gold",
            "currency": result.get("currency", "INR"),
            "unit": "gram",

            "price_24k": round(price_24k, 2),
            "price_22k": round(price_22k, 2),
            "price_18k": round(price_18k, 2),

            "source": "metals.dev",

            "provider_timestamp": provider_timestamp
        }

from decimal import Decimal, ROUND_HALF_UP


class GoldCalculatorService:

    def calculate(
        self,
        purity: int,
        weight_grams: float,
        price_data: dict
    ):

        purity_prices = {
            24: price_data["price_24k"],
            22: price_data["price_22k"],
            18: price_data["price_18k"],
        }

        if purity not in purity_prices:
            raise ValueError(
                "Unsupported purity. Use 24K, 22K or 18K."
            )

        price_per_gram = Decimal(
            str(purity_prices[purity])
        )

        weight = Decimal(
            str(weight_grams)
        )

        gross_value = (
            price_per_gram * weight
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        return {
            "purity": f"{purity}K",
            "weight_grams": float(weight),
            "price_per_gram": float(price_per_gram),
            "gross_gold_value": float(gross_value),
            "currency": price_data["currency"],
            "unit": price_data["unit"],
            "source": price_data["source"],
            "provider_timestamp": price_data["provider_timestamp"]
        }

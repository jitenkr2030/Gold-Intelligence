from decimal import Decimal, ROUND_HALF_UP


class BuybackCalculatorService:

    def calculate(
        self,
        purity: int,
        weight_grams: float,
        buyback_discount_percent: float,
        price_data: dict
    ):

        purity_prices = {
            24: price_data["price_24k"],
            22: price_data["price_22k"],
            18: price_data["price_18k"]
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

        discount_percent = Decimal(
            str(buyback_discount_percent)
        )

        # Gross gold value
        gold_value = (
            price_per_gram * weight
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        # Buyback discount
        discount_amount = (
            gold_value
            * discount_percent
            / Decimal("100")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        # Final estimated buyback value
        buyback_value = (
            gold_value - discount_amount
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        return {
            "purity": f"{purity}K",
            "weight_grams": float(weight),
            "price_per_gram": float(price_per_gram),

            "gold_value": float(gold_value),

            "buyback_discount": {
                "percent": float(discount_percent),
                "amount": float(discount_amount)
            },

            "estimated_buyback_value": float(
                buyback_value
            ),

            "currency": price_data["currency"],
            "unit": price_data["unit"],
            "source": price_data["source"],
            "provider_timestamp": price_data["provider_timestamp"]
        }

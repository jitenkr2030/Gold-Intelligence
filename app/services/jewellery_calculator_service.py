from decimal import Decimal, ROUND_HALF_UP


class JewelleryCalculatorService:

    def calculate(
        self,
        purity: int,
        weight_grams: float,
        wastage_percent: float,
        making_charge_percent: float,
        gst_percent: float,
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

        wastage = Decimal(
            str(wastage_percent)
        )

        making_charge = Decimal(
            str(making_charge_percent)
        )

        gst = Decimal(
            str(gst_percent)
        )

        # Gold value
        gold_value = (
            price_per_gram * weight
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        # Wastage weight
        wastage_weight = (
            weight * wastage / Decimal("100")
        ).quantize(
            Decimal("0.001"),
            rounding=ROUND_HALF_UP
        )

        # Wastage value
        wastage_value = (
            price_per_gram * wastage_weight
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        # Making charges
        making_charge_value = (
            gold_value * making_charge / Decimal("100")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        # Subtotal before GST
        subtotal = (
            gold_value
            + wastage_value
            + making_charge_value
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        # GST
        gst_value = (
            subtotal * gst / Decimal("100")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        # Final jewellery value
        total_value = (
            subtotal + gst_value
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        return {
            "purity": f"{purity}K",
            "weight_grams": float(weight),
            "price_per_gram": float(price_per_gram),

            "gold_value": float(gold_value),

            "wastage": {
                "percent": float(wastage),
                "weight_grams": float(wastage_weight),
                "value": float(wastage_value)
            },

            "making_charges": {
                "percent": float(making_charge),
                "value": float(making_charge_value)
            },

            "subtotal": float(subtotal),

            "gst": {
                "percent": float(gst),
                "value": float(gst_value)
            },

            "total_jewellery_value": float(total_value),

            "currency": price_data["currency"],
            "unit": price_data["unit"],
            "source": price_data["source"],
            "provider_timestamp": price_data["provider_timestamp"]
        }

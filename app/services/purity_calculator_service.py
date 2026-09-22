from decimal import Decimal, ROUND_HALF_UP


class PurityCalculatorService:

    def calculate(
        self,
        purity: int,
        weight_grams: float
    ):

        purity_ratios = {
            24: Decimal("24") / Decimal("24"),
            22: Decimal("22") / Decimal("24"),
            18: Decimal("18") / Decimal("24")
        }

        if purity not in purity_ratios:
            raise ValueError(
                "Unsupported purity. Use 24K, 22K or 18K."
            )

        weight = Decimal(
            str(weight_grams)
        )

        purity_ratio = purity_ratios[purity]

        purity_percent = (
            purity_ratio * Decimal("100")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        pure_gold_weight = (
            weight * purity_ratio
        ).quantize(
            Decimal("0.0001"),
            rounding=ROUND_HALF_UP
        )

        other_metals_weight = (
            weight - pure_gold_weight
        ).quantize(
            Decimal("0.0001"),
            rounding=ROUND_HALF_UP
        )

        return {
            "purity": f"{purity}K",
            "purity_percent": float(purity_percent),
            "total_weight_grams": float(weight),
            "pure_gold_weight_grams": float(pure_gold_weight),
            "other_metals_weight_grams": float(
                other_metals_weight
            )
        }

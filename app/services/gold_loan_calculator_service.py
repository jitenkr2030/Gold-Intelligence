from decimal import Decimal, ROUND_HALF_UP


class GoldLoanCalculatorService:

    def calculate(
        self,
        purity: int,
        weight_grams: float,
        loan_to_value_percent: float,
        interest_rate_percent: float,
        tenure_months: int,
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

        ltv_percent = Decimal(
            str(loan_to_value_percent)
        )

        interest_rate = Decimal(
            str(interest_rate_percent)
        )

        months = Decimal(
            str(tenure_months)
        )

        # Current gold value
        gold_value = (
            price_per_gram * weight
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        # Maximum estimated loan
        eligible_loan_amount = (
            gold_value
            * ltv_percent
            / Decimal("100")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        # Simple interest
        interest_amount = (
            eligible_loan_amount
            * interest_rate
            * months
            / Decimal("1200")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        # Total repayment
        total_repayment = (
            eligible_loan_amount
            + interest_amount
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        return {
            "purity": f"{purity}K",
            "weight_grams": float(weight),
            "price_per_gram": float(price_per_gram),

            "gold_value": float(gold_value),

            "loan": {
                "loan_to_value_percent": float(ltv_percent),
                "eligible_loan_amount": float(
                    eligible_loan_amount
                )
            },

            "interest": {
                "annual_rate_percent": float(
                    interest_rate
                ),
                "tenure_months": int(tenure_months),
                "estimated_interest": float(
                    interest_amount
                )
            },

            "estimated_total_repayment": float(
                total_repayment
            ),

            "currency": price_data["currency"],
            "unit": price_data["unit"],
            "source": price_data["source"],
            "provider_timestamp": price_data["provider_timestamp"]
        }

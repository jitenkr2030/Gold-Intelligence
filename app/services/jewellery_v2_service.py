from decimal import Decimal, ROUND_HALF_UP


class JewelleryPricingV2Service:

    def money(self, value):
        return Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

    def calculate(self, request, price_data):

        purity_prices = {
            24: price_data["price_24k"],
            22: price_data["price_22k"],
            18: price_data["price_18k"],
        }

        if request.purity not in purity_prices:
            raise ValueError(
                "Unsupported purity. Use 24K, 22K or 18K."
            )

        if request.stone_weight_grams > request.gross_weight_grams:
            raise ValueError(
                "Stone weight cannot exceed gross weight."
            )

        making_type = request.making_charge_type.lower().strip()

        if making_type not in {"percent", "fixed"}:
            raise ValueError(
                "making_charge_type must be 'percent' or 'fixed'."
            )

        gross_weight = Decimal(str(request.gross_weight_grams))
        stone_weight = Decimal(str(request.stone_weight_grams))
        wastage_percent = Decimal(str(request.wastage_percent))
        making_charge_input = Decimal(str(request.making_charge))
        stone_charges = Decimal(str(request.stone_charges))
        discount = Decimal(str(request.discount))
        gst_percent = Decimal(str(request.gst_percent))

        net_gold_weight = gross_weight - stone_weight

        price_per_gram = Decimal(
            str(purity_prices[request.purity])
        )

        gold_value = net_gold_weight * price_per_gram

        wastage_weight = (
            net_gold_weight * wastage_percent / Decimal("100")
        )

        wastage_value = wastage_weight * price_per_gram

        gold_plus_wastage = gold_value + wastage_value

        if making_type == "percent":
            making_charge_value = (
                gold_plus_wastage
                * making_charge_input
                / Decimal("100")
            )
        else:
            making_charge_value = making_charge_input

        subtotal = (
            gold_value
            + wastage_value
            + making_charge_value
            + stone_charges
        )

        discount = min(discount, subtotal)

        taxable_amount = subtotal - discount

        gst_value = (
            taxable_amount
            * gst_percent
            / Decimal("100")
        )

        final_price = taxable_amount + gst_value

        return {
            "purity": f"{request.purity}K",
            "currency": price_data["currency"],
            "unit": price_data["unit"],

            "weights": {
                "gross_weight_grams": float(
                    self.money(gross_weight)
                ),
                "stone_weight_grams": float(
                    self.money(stone_weight)
                ),
                "net_gold_weight_grams": float(
                    self.money(net_gold_weight)
                ),
                "wastage_weight_grams": float(
                    self.money(wastage_weight)
                )
            },

            "rates": {
                "gold_rate_per_gram": float(
                    self.money(price_per_gram)
                )
            },

            "charges": {
                "gold_value": float(
                    self.money(gold_value)
                ),
                "wastage_value": float(
                    self.money(wastage_value)
                ),
                "making_charge": float(
                    self.money(making_charge_value)
                ),
                "making_charge_type": making_type,
                "making_charge_input": float(
                    self.money(making_charge_input)
                ),
                "stone_charges": float(
                    self.money(stone_charges)
                )
            },

            "billing": {
                "subtotal": float(
                    self.money(subtotal)
                ),
                "discount": float(
                    self.money(discount)
                ),
                "taxable_amount": float(
                    self.money(taxable_amount)
                ),
                "gst_percent": float(
                    self.money(gst_percent)
                ),
                "gst_amount": float(
                    self.money(gst_value)
                ),
                "final_jewellery_price": float(
                    self.money(final_price)
                )
            },

            "source": price_data["source"],
            "provider_timestamp": price_data[
                "provider_timestamp"
            ]
        }

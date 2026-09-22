from pydantic import BaseModel, Field


class JewelleryPricingV2Request(BaseModel):
    purity: int = Field(
        ...,
        description="Gold purity: 24, 22 or 18",
        examples=[22]
    )

    gross_weight_grams: float = Field(
        ...,
        gt=0,
        description="Total jewellery weight including stones",
        examples=[25]
    )

    stone_weight_grams: float = Field(
        default=0,
        ge=0,
        description="Weight of stones/non-gold material",
        examples=[2]
    )

    wastage_percent: float = Field(
        default=0,
        ge=0,
        le=100,
        description="Wastage percentage applied to net gold weight",
        examples=[5]
    )

    making_charge: float = Field(
        default=0,
        ge=0,
        description="Making charge. Percentage or fixed amount depending on making_charge_type",
        examples=[10]
    )

    making_charge_type: str = Field(
        default="percent",
        description="Making charge type: percent or fixed",
        examples=["percent"]
    )

    stone_charges: float = Field(
        default=0,
        ge=0,
        description="Direct stone/gem charges in currency",
        examples=[5000]
    )

    discount: float = Field(
        default=0,
        ge=0,
        description="Discount amount deducted before GST",
        examples=[5000]
    )

    gst_percent: float = Field(
        default=0,
        ge=0,
        le=100,
        description="GST/tax percentage supplied by the caller",
        examples=[3]
    )

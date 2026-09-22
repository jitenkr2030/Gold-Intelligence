from pydantic import BaseModel, Field


class BuybackCalculationRequest(BaseModel):

    purity: int = Field(
        ...,
        description="Gold purity. Supported: 24, 22, 18",
        examples=[22]
    )

    weight_grams: float = Field(
        ...,
        gt=0,
        description="Gold weight in grams",
        examples=[25]
    )

    buyback_discount_percent: float = Field(
        default=0,
        ge=0,
        le=100,
        description="Buyback discount percentage",
        examples=[5]
    )

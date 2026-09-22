from pydantic import BaseModel, Field


class JewelleryCalculationRequest(BaseModel):

    purity: int = Field(
        ...,
        description="Gold purity. Supported: 24, 22, 18",
        examples=[22]
    )

    weight_grams: float = Field(
        ...,
        gt=0,
        description="Net gold weight in grams",
        examples=[25]
    )

    wastage_percent: float = Field(
        default=0,
        ge=0,
        le=100,
        description="Wastage percentage",
        examples=[5]
    )

    making_charge_percent: float = Field(
        default=0,
        ge=0,
        description="Making charge percentage",
        examples=[10]
    )

    gst_percent: float = Field(
        default=0,
        ge=0,
        description="GST percentage supplied by the caller",
        examples=[3]
    )

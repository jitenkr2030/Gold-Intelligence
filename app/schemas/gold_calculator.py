from pydantic import BaseModel, Field


class GoldCalculationRequest(BaseModel):
    purity: int = Field(
        ...,
        description="Gold purity in karat. Supported: 24, 22, 18",
        examples=[22]
    )

    weight_grams: float = Field(
        ...,
        gt=0,
        description="Gold weight in grams",
        examples=[25]
    )

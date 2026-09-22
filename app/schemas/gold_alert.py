from pydantic import BaseModel, Field


class GoldAlertCreateRequest(BaseModel):

    purity: int = Field(
        ...,
        description="Gold purity. Supported: 24, 22, 18",
        examples=[22]
    )

    target_price: float = Field(
        ...,
        gt=0,
        description="Target gold price per gram",
        examples=[12000]
    )

    condition: str = Field(
        ...,
        description="Alert condition: above or below",
        examples=["below"]
    )

    currency: str = Field(
        default="INR",
        description="Currency",
        examples=["INR"]
    )

    unit: str = Field(
        default="gram",
        description="Price unit",
        examples=["gram"]
    )

from pydantic import BaseModel, Field


class GoldLoanCalculationRequest(BaseModel):

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

    loan_to_value_percent: float = Field(
        default=75,
        gt=0,
        le=100,
        description="Loan-to-value percentage",
        examples=[75]
    )

    interest_rate_percent: float = Field(
        default=12,
        ge=0,
        description="Annual interest rate percentage",
        examples=[12]
    )

    tenure_months: int = Field(
        default=12,
        gt=0,
        description="Loan tenure in months",
        examples=[12]
    )

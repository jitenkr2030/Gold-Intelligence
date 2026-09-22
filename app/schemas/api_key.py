from pydantic import BaseModel, Field


class APIKeyCreateRequest(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Name identifying this API key",
        examples=["My WordPress Plugin"]
    )

    plan: str = Field(
        default="free",
        description="API plan: free, developer, business",
        examples=["free"]
    )

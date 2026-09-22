from pydantic import BaseModel, Field


class GoldWebhookCreateRequest(BaseModel):

    url: str = Field(
        ...,
        min_length=8,
        description="Webhook URL",
        examples=["https://example.com/webhook"]
    )

    event: str = Field(
        default="gold_alert_triggered",
        description="Webhook event",
        examples=["gold_alert_triggered"]
    )

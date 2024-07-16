"""Service Contracts."""

from pydantic import (
    BaseModel,
    Field,
)


class PredictionRequest(BaseModel):
    """Prediction request contract."""

    tx_datetime: int = Field(..., description="Unix timestamp in milliseconds")
    tx_amount: float = Field(..., description="Transaction amount")
    customer_id_mean_tx_amount_5_days: float = Field(
        ...,
        description="Mean transaction amount for customer in the last 1 day",
    )
    terminal_id_mean_tx_fraud_5_days: float = Field(
        ...,
        description="Mean transaction amount for customer in the last 1 day",
    )

    class Config:
        """Schema configurations for examples."""

        schema_extra = {
            "example": {
                "tx_datetime": 1672271365000,
                "tx_amount": 120.5,
                "customer_id_mean_tx_amount_5_days": 110.0,
                "terminal_id_mean_tx_fraud_5_days": 5,
            }
        }


class PredictionResponse(BaseModel):
    """Prediction contract."""

    transaction_id: str = Field(
        ..., description="Unique Identifier transaction."
    )
    transaction_to_block: int = Field(
        ..., description="(1 = we block the transaction, 0 = we don't)"
    )

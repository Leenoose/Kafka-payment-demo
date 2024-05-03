from pydantic import BaseModel
from typing import Optional


class Transaction(BaseModel):
    transaction_id: int
    sender_id: int
    recipient_id: int
    amount: float

from pydantic import BaseModel
from typing import Optional


class Transaction_Topic(BaseModel):
    sender_id: int
    recipient_id: int
    amount: float
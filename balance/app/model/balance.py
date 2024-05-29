from pydantic import BaseModel
from typing import Optional


class Balance(BaseModel):
    user_id: int
    balance: float

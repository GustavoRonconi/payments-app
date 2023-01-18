from pydantic import BaseModel
from typing import Optional


class PaymentDebt(BaseModel):
    debt_id: int
    name: str
    government_id: int
    email: str
    debt_amount: float
    debt_due_date: str
    status: Optional[str] = "open"

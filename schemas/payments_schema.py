from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class payment_schema(BaseModel):
    order_id: int
    provider: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[Decimal] = None
    created_at: Optional[datetime] = None
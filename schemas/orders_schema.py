from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class order_schema(BaseModel):
    user_id: int
    status: str
    total: Decimal
    created_at: Optional[datetime] = None
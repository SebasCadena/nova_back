from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class carrito_schema(BaseModel):
    user_id: int
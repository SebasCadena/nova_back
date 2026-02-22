from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class product_schema(BaseModel):
    name: str
    slug: str
    description: str
    price: Decimal
    image_url: str
    category_id: int
    is_active: bool
    #create_at
    #update_at
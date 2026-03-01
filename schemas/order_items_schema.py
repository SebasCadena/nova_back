from decimal import Decimal
from pydantic import BaseModel

class order_item_schema(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: Decimal
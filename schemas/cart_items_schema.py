from pydantic import BaseModel

class cart_item_schema(BaseModel):
    cart_id: int
    product_id: int
    quantity: int
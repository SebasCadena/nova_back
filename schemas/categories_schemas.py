from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class category_schema(BaseModel):
    name: str
    slug: str
    

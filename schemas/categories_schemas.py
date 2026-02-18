from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class category(BaseModel):
    name: str
    slug: str
    #create_at
    #update_at

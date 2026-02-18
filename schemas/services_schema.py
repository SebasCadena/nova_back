from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class service(BaseModel):
    title: str
    slug: str
    description: str
    icon: str
    is_active: bool
    #create_at
    #update_at

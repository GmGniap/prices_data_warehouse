## Pydantic Models
from pydantic import BaseModel
from datetime import datetime


class GreenwayBase(BaseModel):
    id: int
    created_at: datetime
    crop: str
    crop_id: int
    crop_location: str | None
    crop_name: str | None
    market: str | None
    price: str | None
    remark: str | None
    state_id: int
    tab_date: str | None
    tab_name: str | None
    township: str | None
    township_id: int
    unit: str | None
    updated_at: datetime

    class Config:
        orm_mode = True


class GreenwayCreate(GreenwayBase):
    pass

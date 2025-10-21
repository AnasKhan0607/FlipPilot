from pydantic import BaseModel

class Item(BaseModel):
    id: str
    title: str
    price_cents: int
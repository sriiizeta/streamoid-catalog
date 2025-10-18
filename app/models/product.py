# app/models/product.py
from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal, InvalidOperation
from pydantic import model_validator

class ProductBase(SQLModel):
    sku: str = Field(..., max_length=100)
    name: str
    brand: str
    color: Optional[str] = None
    size: Optional[str] = None
    mrp: Decimal
    price: Decimal
    quantity: Optional[int] = 0

    @model_validator(mode='after')
    def check_price_and_quantity(cls, model):
        # model is the validated instance
        mrp = model.mrp
        price = model.price
        qty = model.quantity
        if mrp is None or price is None:
            raise ValueError("mrp and price are required")
        try:
            # Decimal comparability
            if price > mrp:
                raise ValueError("price must be <= mrp")
        except InvalidOperation:
            raise ValueError("invalid numeric value for mrp/price")
        if qty is not None and int(qty) < 0:
            raise ValueError("quantity must be >= 0")
        return model

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sku: str = Field(..., index=True, unique=True)

class ProductRead(ProductBase):
    id: int

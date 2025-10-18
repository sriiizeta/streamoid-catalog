from app.models.product import ProductBase
from decimal import Decimal
import pytest

def test_price_less_than_mrp_ok():
    p = ProductBase(sku="A", name="a", brand="b", mrp=Decimal("100.00"), price=Decimal("90.00"), quantity=1)
    assert p.price <= p.mrp

def test_price_greater_than_mrp_fails():
    with pytest.raises(ValueError):
        ProductBase(sku="A", name="a", brand="b", mrp=Decimal("100.00"), price=Decimal("120.00"), quantity=1)

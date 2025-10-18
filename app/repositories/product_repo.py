from sqlmodel import select
from sqlmodel import Session
from typing import List, Optional
from app.models.product import Product

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def bulk_insert(self, products: List[Product], chunk: int = 500):
        for i in range(0, len(products), chunk):
            self.session.add_all(products[i:i+chunk])
            self.session.commit()
        # refresh not needed for bulk inserts

    def list_products(self, page: int = 1, limit: int = 20):
        offset = (page - 1) * limit
        stmt = select(Product).offset(offset).limit(limit)
        total = self.session.exec(select(Product).count()).one()
        rows = self.session.exec(stmt).all()
        return {"total": total, "items": rows}

    def search(self, brand: Optional[str]=None, color: Optional[str]=None,
               min_price: Optional[float]=None, max_price: Optional[float]=None,
               page: int=1, limit: int=20):
        stmt = select(Product)
        if brand:
            stmt = stmt.where(Product.brand == brand)
        if color:
            stmt = stmt.where(Product.color == color)
        if min_price is not None:
            stmt = stmt.where(Product.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Product.price <= max_price)
        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        rows = self.session.exec(stmt).all()
        return {"items": rows}

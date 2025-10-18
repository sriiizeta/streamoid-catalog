import csv, codecs
from decimal import Decimal, InvalidOperation
from typing import List, Dict
from io import TextIOBase
from app.models.product import Product, ProductBase
from sqlmodel import Session

def parse_decimal(s):
    try:
        return Decimal(s.strip())
    except (InvalidOperation, AttributeError):
        raise ValueError("invalid decimal")

def process_csv_stream(file_stream, session: Session):
    """
    Reads CSV stream line by line, validates with ProductBase, returns stored_count and failures.
    file_stream: bytes stream from UploadFile.file
    """
    text_iter = codecs.iterdecode(file_stream, "utf-8")
    reader = csv.DictReader(text_iter)
    valid_products = []
    failures = []
    row_no = 1  # adjust if header

    for row in reader:
        row_no += 1
        try:
            # required fields check
            for fld in ("sku","name","brand","mrp","price"):
                if not row.get(fld):
                    raise ValueError(f"{fld} required")
            # coerce and create model dict
            payload = {
                "sku": row["sku"].strip(),
                "name": row["name"].strip(),
                "brand": row["brand"].strip(),
                "color": row.get("color") and row["color"].strip(),
                "size": row.get("size") and row["size"].strip(),
                "mrp": parse_decimal(row["mrp"]),
                "price": parse_decimal(row["price"]),
                "quantity": int(row["quantity"]) if row.get("quantity") not in (None,"") else 0
            }
            validated = ProductBase(**payload)
            product = Product(**validated.dict())
            valid_products.append(product)
        except Exception as e:
            failures.append({"row": row_no, "sku": row.get("sku"), "reason": str(e)})

    # persist valid products in bulk (repository or session)
    if valid_products:
        session.add_all(valid_products)
        session.commit()

    return {
        "total_processed": row_no - 1,
        "stored": len(valid_products),
        "failed_count": len(failures),
        "failed": failures
    }

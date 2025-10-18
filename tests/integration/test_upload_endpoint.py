from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_upload_and_list():
    csv_data = "sku,name,brand,mrp,price,quantity\nA,Item A,BrandX,100,90,5\n"
    files = {"file": ("products.csv", csv_data, "text/csv")}
    resp = client.post("/upload", files=files)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stored"] >= 1
    # list
    resp2 = client.get("/products")
    assert resp2.status_code == 200

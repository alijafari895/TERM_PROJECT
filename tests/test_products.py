# test products
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_product():
    response = client.post("/products/", json={
        "name": "Laptop",
        "sku": "SKU123",
        "price": 1500,
        "min_threshold": 5,
        "category": "Electronics"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["sku"] == "SKU123"

def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

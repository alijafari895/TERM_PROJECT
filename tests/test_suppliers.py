# test suppliers
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_supplier():
    response = client.post("/suppliers/", json={
        "name": "Supplier1",
        "email": "supplier@example.com",
        "phone": "123456789",
        "delivery_time": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Supplier1"

def test_get_suppliers():
    response = client.get("/suppliers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

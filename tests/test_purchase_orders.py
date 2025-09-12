# test purchase orders
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_purchase_order():
    response = client.post("/purchase-orders/", json={
        "supplier_id": 1,
        "items": [
            {"sku": "SKU123", "quantity": 10}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "draft"

def test_update_purchase_order_status():
    response = client.put("/purchase-orders/1", json={"status": "received"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"

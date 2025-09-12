# test users
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_user_signup_and_login():
    # signup
    response = client.post("/users/signup", json={
        "full_name": "Test User",
        "email": "test@example.com",
        "username": "testuser",
        "password": "test1234"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

    # login
    response = client.post("/users/login", data={
        "username": "testuser",
        "password": "test1234"
    })
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_account_balance():
    response = client.get("/get_account_balance/ADDRESS")
    assert response.status_code == 200
    assert "address" in response.json()
    assert "balance" in response.json()

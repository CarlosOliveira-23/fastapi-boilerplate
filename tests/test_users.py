from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Boilerplate FastAPI funcionando!"}


def test_user_registration():
    response = client.post("/users/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"

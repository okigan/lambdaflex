from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_read_root():
    print("xxxx\n")
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_pets():
    print("xxxx\n")
    response = client.get("/pets")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Dog", "category": "Mammal", "price": 500.0}, 
        {"id": 2, "name": "Cat", "category": "Mammal", "price": 300.0},
        {"id": 3, "name": "Parrot", "category": "Bird", "price": 150.0}
    ]

from mmo.main import app 
from fastapi.testclient import TestClient

class CustomClient(TestClient):
    def __init__(self, app):
        super().__init__(app)
        self.headers["Is-Testing"] = "True"

    def get(self, *args, **kwargs):
        return self.request("GET", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request("DELETE", *args, **kwargs)

client = CustomClient(app)

def test_delete():
    response = client.delete(
        "/api/v1/auth/delete",
        json={
            "username": "test",
            "password": "test"
        }
    )
    json = response.json()

    # User may or may not exist, so we don't care about the status code
    assert response.status_code not in [422, 500]

def test_signup():
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "test",
            "password": "test"
        }
    )
    json = response.json()

    assert response.status_code == 201
    assert "message" in json
    assert "data" in json
    assert "access_token" in json["data"]
    assert "token_type" in json["data"]
    assert json["data"]["token_type"] == "bearer"

    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "test",
            "password": "test"
        }
    )
    json = response.json()

    assert response.status_code == 409
    assert "detail" in json


def test_login():
    response = client.get(
        "/api/v1/auth/login",
        json={
            "username": "test",
            "password": "test"
        }
    )
    json = response.json()

    assert response.status_code == 200
    assert "message" in json
    assert "data" in json
    assert "access_token" in json["data"]
    assert "token_type" in json["data"]
    assert json["data"]["token_type"] == "bearer"

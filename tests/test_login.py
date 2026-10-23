import sys
import os 

import jwt
import pytest

from src.auth_helper import JWT_SECRET, ALGORITHM
from fastapi.testclient import TestClient

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_login_existing_user_returns_jwt(client):
    payload = {
        "email": "alice@example.com",
        "password": "password123",
    }

    response = client.post("/api/auth/login", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)
    assert len(data["token"]) > 0

    decoded = jwt.decode(
        data["token"],
        JWT_SECRET,
        algorithms=[ALGORITHM],
    )
    assert decoded.get("sub") is not None


def test_login_unknown_email_returns_401(client):
    payload = {
        "email": "unknown@example.com",
        "password": "securepassword123",
    }

    response = client.post("/api/auth/login", json=payload)

    assert response.status_code == 401


def test_login_incorrect_password_returns_401(client):
    payload = {
        "email": "alice@example.com",
        "password": "wrongpassword",
    }

    response = client.post("/api/auth/login", json=payload)

    assert response.status_code == 401


def test_login_invalid_credentials_have_same_error(client):
    unknown_email_response = client.post(
        "/api/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "securepassword123",
        },
    )

    wrong_password_response = client.post(
        "/api/auth/login",
        json={
            "email": "alice@example.com",
            "password": "wrongpassword",
        },
    )

    assert unknown_email_response.status_code == 401
    assert wrong_password_response.status_code == 401
    assert unknown_email_response.json() == wrong_password_response.json()


def test_login_does_not_return_password(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "alice@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    assert "password" not in response.json()
    assert "securepassword123" not in response.text
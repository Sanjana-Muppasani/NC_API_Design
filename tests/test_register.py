import os
import sys
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_register_new_user(client): 
    payload = {
        "name": "Graham Morgan",
        "email": "graham@example.com",
        "password": "securepassword123"
    }
    
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert "user" in data
    user = data["user"]

    assert user["name"] == payload["name"]
    assert user["email"] == payload["email"]
    assert "id" in user
    assert "created_at" in user
    assert "password" not in user
    assert "password_hash" not in user 
    assert payload["password"] not in response.text 

def test_register_duplicate_email(client):
    payload = {
        "name": "Harry Smith",
        "email": "harry@example.com",
        "password": "securepassword123"
    }

    first_response = client.post("/api/auth/register", json=payload)
    assert first_response.status_code == 201

    second_response = client.post(
        "/api/auth/register",
        json={
            "name": "Harry Jones",
            "email": "harry@example.com",
            "password": "anotherpassword123"
        }
    )

    assert second_response.status_code == 409
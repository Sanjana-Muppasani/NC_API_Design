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

def parse_datetime(value): 
    return datetime.isoformat(value)
def test_get_events_returns_200(client):
    response = client.get("/api/events")
    assert response.status_code == 200


def test_get_events_returns_events_object(client):
    response = client.get("/api/events")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "events" in data
    assert isinstance(data["events"], list)


def test_get_events_returns_top_5_seeded_events(client):
    response = client.get("/api/events")

    assert response.status_code == 200

    events = response.json()["events"]
    assert len(events) >= 5

    top_5_events = events[:5]

    expected_titles = [
        "Leeds Tech Meetup – June Edition",
        "Intro to Machine Learning Workshop",
        "Northern Power Women in Tech",
        "Brighton Python Meetup",
        "API Design Patterns",
    ]

    actual_titles = [event["title"] for event in top_5_events]

    assert actual_titles == expected_titles


def test_events_contains_required_fields(client):
    response = client.get("/api/events")

    assert response.status_code == 200

    events = response.json()["events"]

    required_fields = {
        "id",
        "title",
        "starts_at",
        "ends_at",
        "location",
    }

    for event in events:
        assert required_fields.issubset(event.keys())

        assert isinstance(event["id"], int)
        assert isinstance(event["title"], str)
        assert event["location"] is None or isinstance(
        event["location"], str
    )

        starts_at = datetime.fromisoformat(event["starts_at"])
        ends_at = datetime.fromisoformat(event["ends_at"])

        assert starts_at.tzinfo is not None
        assert ends_at.tzinfo is not None
        assert starts_at < ends_at
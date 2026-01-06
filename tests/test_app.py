import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Basketball"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")
    # Try signing up again (should fail)
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_unregister_participant():
    email = "testuser2@mergington.edu"
    activity = "Soccer"
    # Sign up first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Unregistered")
    # Try unregistering again (should fail)
    response2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 400
    assert "not registered" in response2.json()["detail"]

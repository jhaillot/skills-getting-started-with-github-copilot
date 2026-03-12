from copy import deepcopy

from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities state between tests."""
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_get_activities_returns_ids():
    # Arrange: nothing to prepare beyond the default in-memory state

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert all(isinstance(k, str) for k in data.keys())
    for info in data.values():
        assert "name" in info


def test_signup_and_remove_flow():
    # Arrange
    activity_id = next(iter(activities.keys()))
    original_name = activities[activity_id]["name"]
    email = "newstudent@mergington.edu"

    # Ensure a clean starting state for this email
    if email in activities[activity_id]["participants"]:
        activities[activity_id]["participants"].remove(email)

    # Act: sign up
    signup_resp = client.post(
        f"/activities/{activity_id}/signup",
        json={"email": email},
    )

    # Assert: sign up succeeded
    assert signup_resp.status_code == 200
    assert original_name in signup_resp.json()["message"]
    assert email in activities[activity_id]["participants"]

    # Act: remove
    remove_resp = client.delete(
        f"/activities/{activity_id}/participants",
        json={"email": email},
    )

    # Assert: removal succeeded
    assert remove_resp.status_code == 200
    assert email not in activities[activity_id]["participants"]


def test_nonexistent_activity_returns_404():
    # Arrange
    invalid_id = "not-a-real-activity"

    # Act
    response = client.post(
        f"/activities/{invalid_id}/signup",
        json={"email": "x@x.com"},
    )

    # Assert
    assert response.status_code == 404

from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_ids():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()

    # should be a dictionary keyed by ids
    assert isinstance(data, dict)
    assert all(isinstance(k, str) for k in data.keys())
    # each value should have a name field
    for info in data.values():
        assert "name" in info


def test_signup_and_remove_flow():
    # pick one of the activity ids from the in-memory data
    activity_id = next(iter(activities.keys()))
    original_name = activities[activity_id]["name"]
    email = "newstudent@mergington.edu"

    # ensure email is not already there
    if email in activities[activity_id]["participants"]:
        activities[activity_id]["participants"].remove(email)

    resp = client.post(
        f"/activities/{activity_id}/signup",
        json={"email": email},
    )
    assert resp.status_code == 200
    assert original_name in resp.json()["message"]
    assert email in activities[activity_id]["participants"]

    # try removing the participant
    del_resp = client.delete(
        f"/activities/{activity_id}/participants",
        json={"email": email},
    )
    assert del_resp.status_code == 200
    assert email not in activities[activity_id]["participants"]


def test_old_name_path_no_longer_works():
    # using a human-readable name should produce 404
    sample_name = activities[next(iter(activities.keys()))]["name"]
    resp = client.post(f"/activities/{sample_name}/signup", params={"email": "x@x.com"})
    assert resp.status_code == 404

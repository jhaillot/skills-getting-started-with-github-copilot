"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database keyed by **ID** instead of human-readable label. Each entry
# includes a `name` property for display. Using identifiers keeps URLs stable even if the
# name changes, and avoids problems when names contain spaces or special characters.
activities = {
    "chess-club": {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "programming-class": {
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "gym-class": {
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "basketball-team": {
        "name": "Basketball Team",
        "description": "Competitive basketball practice and games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "tennis-club": {
        "name": "Tennis Club",
        "description": "Tennis lessons and friendly matches",
        "schedule": "Saturdays, 9:00 AM - 11:00 AM",
        "max_participants": 10,
        "participants": ["lucas@mergington.edu"]
    },
    "art-studio": {
        "name": "Art Studio",
        "description": "Painting, drawing, and sculpture techniques",
        "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "noah@mergington.edu"]
    },
    "drama-club": {
        "name": "Drama Club",
        "description": "Theater productions and acting workshops",
        "schedule": "Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 25,
        "participants": ["ava@mergington.edu"]
    },
    "debate-team": {
        "name": "Debate Team",
        "description": "Develop public speaking and critical thinking skills",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["mason@mergington.edu", "chloe@mergington.edu"]
    },
    "science-club": {
        "name": "Science Club",
        "description": "Explore physics, chemistry, and biology through experiments",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["ethan@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Return the full activities map. Clients can use the returned IDs when
    forming URLs to sign up or remove participants."""
    return activities
from pydantic import BaseModel


class EmailPayload(BaseModel):
    email: str


@app.delete("/activities/{activity_id}/participants")
def remove_participant(activity_id: str, payload: EmailPayload):
    """Remove a student (identified by email) from an activity.

    For GDPR reasons the email is supplied in the body rather than the URL.
    """
    email = payload.email

    if activity_id not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_id]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity['name']}"}


@app.post("/activities/{activity_id}/signup")
def signup_for_activity(activity_id: str, payload: EmailPayload):
    """Sign up a student for an activity using the activity **ID**

    The email address is provided in the JSON request body rather than a
    query parameter to avoid leaking personal data in URLs (GDPR compliance).
    """
    email = payload.email

    # Validate activity exists by id
    if activity_id not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_id]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity['name']}"}

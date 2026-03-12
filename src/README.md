# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                                   | Description                                                         |
| ------ | --------------------------------------------------------------------------| ------------------------------------------------------------------- |
| GET    | `/activities`                                                              | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_id}/signup`                                      | Sign up for an activity (email in JSON body)                      |
| DELETE | `/activities/{activity_id}/participants`                               | Remove a student from an activity (email in JSON body)             |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses an internal **ID** as the identifier (the
   human-readable name is stored in the `name` field). This makes URLs more
   stable and avoids issues with spaces or changing titles.

   - Name (for display purposes)
   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.

> **Privacy note:** email addresses are now sent in the request body rather than
> query parameters to avoid exposing personal data in logs or browser history.

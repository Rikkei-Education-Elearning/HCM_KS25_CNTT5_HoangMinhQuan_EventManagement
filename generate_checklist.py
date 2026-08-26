import pandas as pd
import os

data = [
    ["Auth", "/auth/register", "POST", "Register new user with valid data", "Happy Path", "Status 201 Created, returns user info"],
    ["Auth", "/auth/register", "POST", "Register with already existing email/username", "Error", "Status 400/409, Error message"],
    ["Auth", "/auth/register", "POST", "Register with missing required fields", "Error", "Status 422 Unprocessable Entity"],
    ["Auth", "/auth/login", "POST", "Login with valid username and password", "Happy Path", "Status 200 OK, returns access & refresh tokens"],
    ["Auth", "/auth/login", "POST", "Login with incorrect password", "Error", "Status 401 Unauthorized"],
    ["Auth", "/auth/login", "POST", "Login with non-existent username", "Error", "Status 401 Unauthorized"],
    ["Auth", "/auth/refresh", "POST", "Refresh token with valid refresh_token", "Happy Path", "Status 200 OK, returns new tokens"],
    ["Auth", "/auth/refresh", "POST", "Refresh token with invalid/expired refresh_token", "Error", "Status 401 Unauthorized"],
    
    ["Users", "/users/me", "GET", "Get current user profile with valid token", "Happy Path", "Status 200 OK, returns user profile"],
    ["Users", "/users/me", "GET", "Get current user profile without token", "Error", "Status 401 Unauthorized"],
    
    ["Events", "/events", "POST", "Create new event with valid data (name, description, etc)", "Happy Path", "Status 201 Created, returns event info"],
    ["Events", "/events", "POST", "Create event with missing required fields", "Error", "Status 422 Unprocessable Entity"],
    ["Events", "/events", "POST", "Create event without authentication token", "Error", "Status 401 Unauthorized"],
    
    ["Events", "/events", "GET", "Get list of events (query by name or owner)", "Happy Path", "Status 200 OK, returns list of events"],
    ["Events", "/events/{event_id}", "GET", "Get event details by valid event_id", "Happy Path", "Status 200 OK, returns event details"],
    ["Events", "/events/{event_id}", "GET", "Get event details with non-existent event_id", "Error", "Status 404 Not Found"],
    
    ["Events", "/events/{event_id}", "PUT", "Update event fully with valid data & owner token", "Happy Path", "Status 200 OK, returns updated event"],
    ["Events", "/events/{event_id}", "PUT", "Update event without owner permissions", "Error", "Status 403 Forbidden"],
    
    ["Events", "/events/{event_id}", "PATCH", "Partially update event with valid data", "Happy Path", "Status 200 OK, returns updated event"],
    
    ["Events", "/events/{event_id}", "DELETE", "Delete event with valid owner token", "Happy Path", "Status 204 No Content"],
    ["Events", "/events/{event_id}", "DELETE", "Delete event without owner permissions", "Error", "Status 403 Forbidden"],
    
    ["Event Members", "/events/{event_id}/members", "POST", "Add a valid user to the event", "Happy Path", "Status 201 Created"],
    ["Event Members", "/events/{event_id}/members", "POST", "Add a user that is already a member", "Error", "Status 400 Bad Request"],
    ["Event Members", "/events/{event_id}/members", "POST", "Add a non-existent user to the event", "Error", "Status 404 Not Found"],
    
    ["Event Members", "/events/{event_id}/members", "GET", "Get list of members of an event with pagination", "Happy Path", "Status 200 OK, returns member list"],
    
    ["Event Members", "/events/{event_id}/members/{user_id}", "DELETE", "Remove a member from the event", "Happy Path", "Status 204 No Content"],
    ["Event Members", "/events/{event_id}/members/{user_id}", "DELETE", "Remove a member without owner permissions", "Error", "Status 403 Forbidden"],
    
    ["Event Tasks", "/events/{event_id}/event-tasks", "POST", "Create a task for an event with valid data", "Happy Path", "Status 201 Created"],
    ["Event Tasks", "/events/{event_id}/event-tasks", "POST", "Create a task with invalid assignee", "Error", "Status 400/404 Error"],
    
    ["Event Tasks", "/events/{event_id}/event-tasks", "GET", "Get list of tasks for an event with pagination", "Happy Path", "Status 200 OK, returns task list"],
    
    ["Event Tasks", "/event-tasks/{id}", "GET", "Get specific event task details by id", "Happy Path", "Status 200 OK"],
    ["Event Tasks", "/event-tasks/{id}", "GET", "Get non-existent event task", "Error", "Status 404 Not Found"],
    
    ["Event Tasks", "/event-tasks/{id}", "PATCH", "Update task details/status", "Happy Path", "Status 200 OK, returns updated task"],
    
    ["Event Tasks", "/event-tasks/{id}", "DELETE", "Delete a task by id", "Happy Path", "Status 200 OK"],
]

df = pd.DataFrame(data, columns=["Module", "Endpoint", "Method", "Test Case Description", "Test Type", "Expected Result"])
df["Status (Pass/Fail)"] = ""
df["Notes"] = ""

output_file = "API_Test_Checklist.xlsx"
df.to_excel(output_file, index=False)
print(f"Checklist generated successfully at {os.path.abspath(output_file)}")

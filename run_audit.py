import json
import httpx
import uuid
import datetime
import jwt
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.user import User
from app.models.event import Event
from app.models import EventStaff
from app.models.event_task import EventTask
from sqlalchemy import text

client = TestClient(app)
db = SessionLocal()

results = []
def record(test_group, test_case, input_desc, expected, actual, status_code, result, notes=""):
    results.append({
        "group": test_group,
        "case": test_case,
        "input": input_desc,
        "expected": expected,
        "actual": str(actual)[:200],
        "status": status_code,
        "result": result,
        "notes": notes
    })
    print(f"[{result}] {test_group} - {test_case} (Status: {status_code})")

def rand_email():
    return f"test_{uuid.uuid4().hex[:8]}@example.com"

# ==========================================
# SETUP
# ==========================================
email1 = rand_email()
pw = "Password123"
client.post("/auth/register", data={"email": email1, "full_name": "Test User 1", "password": pw})
res = client.post("/auth/login", data={"username": email1, "password": pw})
token1 = res.json()["data"]["access_token"]
headers1 = {"Authorization": f"Bearer {token1}"}

email2 = rand_email()
client.post("/auth/register", data={"email": email2, "full_name": "Test User 2", "password": pw})
res = client.post("/auth/login", data={"username": email2, "password": pw})
token2 = res.json()["data"]["access_token"]
headers2 = {"Authorization": f"Bearer {token2}"}

email3 = rand_email()
client.post("/auth/register", data={"email": email3, "full_name": "Test User 3", "password": pw})
res = client.post("/auth/login", data={"username": email3, "password": pw})
token3 = res.json()["data"]["access_token"]
headers3 = {"Authorization": f"Bearer {token3}"}

# Create Event A (owner: user1)
evA_payload = {"name": "Event A", "description": "Desc A", "location": "Loc A", "start_time": "2026-01-01T00:00:00", "end_time": "2026-01-02T00:00:00", "status": "DRAFT", "event_type": "CONFERENCE", "capacity": 100, "created_at": "2026-01-01T00:00:00"}
res_evA = client.post("/events", data=evA_payload, headers=headers1)
if res_evA.status_code != 201: print("Event A failed:", res_evA.text)
eventA_id = res_evA.json()["data"]["id"]

# Create Event B (owner: user2)
evB_payload = {"name": "Event B", "description": "Desc B", "location": "Loc B", "start_time": "2026-01-01T00:00:00", "end_time": "2026-01-02T00:00:00", "status": "DRAFT", "event_type": "CONFERENCE", "capacity": 100, "created_at": "2026-01-01T00:00:00"}
res_evB = client.post("/events", data=evB_payload, headers=headers2)
if res_evB.status_code != 201: print("Event B failed:", res_evB.text)
eventB_id = res_evB.json()["data"]["id"]

# Get user IDs
u1_id = db.query(User).filter(User.email == email1).first().id
u2_id = db.query(User).filter(User.email == email2).first().id
u3_id = db.query(User).filter(User.email == email3).first().id

# Add user 3 to Event A as staff
client.post(f"/events/{eventA_id}/members", data={"user_id": u3_id}, headers=headers1)

# Add Task A to Event A (assigned to u1) via API (which returns 500)
try:
    res_taskA = client.post(f"/events/{eventA_id}/event-tasks", data={"event_id": eventA_id, "assignee_id": u1_id, "title": "Task A", "description": "A", "status": "pending", "priority": "medium", "due_date": "2026-01-01T00:00:00", "created_at": "2026-01-01T00:00:00"}, headers=headers1)
    if res_taskA.status_code == 500:
        record("11. EVENT TASK 500 ERRORS", "Create Task", "POST /event-tasks", "201 Created", res_taskA.text, 500, "FAIL")
except Exception as e:
    record("11. EVENT TASK 500 ERRORS", "Create Task", "POST /event-tasks", "201 Created", str(e), 500, "FAIL")

# Direct DB insertion to unblock further tests
taskA = EventTask(event_id=eventA_id, assignee_id=u1_id, title="Task A", description="A", status="pending", priority="medium", due_date=datetime.datetime(2026, 1, 1), created_at=datetime.datetime(2026, 1, 1))
taskB = EventTask(event_id=eventB_id, assignee_id=u2_id, title="Task B", description="B", status="pending", priority="medium", due_date=datetime.datetime(2026, 1, 1), created_at=datetime.datetime(2026, 1, 1))
db.add_all([taskA, taskB])
db.commit()
db.refresh(taskA)
db.refresh(taskB)
taskA_id = taskA.id
taskB_id = taskB.id


# ==========================================
# 1. AUTH REGISTER (partial, handled above)
# ==========================================

# ==========================================
# 3. GET EVENT BY ID
# ==========================================
# Owner
r = client.get(f"/events/{eventA_id}", headers=headers1)
record("3. GET EVENT BY ID", "Owner", "GET /events/A", "200 OK", r.text, r.status_code, "PASS" if r.status_code == 200 else "FAIL")

# Staff (User 3)
r = client.get(f"/events/{eventA_id}", headers=headers3)
record("3. GET EVENT BY ID", "Staff member", "GET /events/A", "200 OK", r.text, r.status_code, "PASS" if r.status_code == 200 else "FAIL")

# Unrelated User (User 2)
r = client.get(f"/events/{eventA_id}", headers=headers2)
record("3. GET EVENT BY ID", "Unrelated auth user", "GET /events/A", "403 Forbidden", r.text, r.status_code, "PASS" if r.status_code in [403, 401] else "FAIL")

# Unauthenticated
r = client.get(f"/events/{eventA_id}")
record("3. GET EVENT BY ID", "Unauthenticated", "GET /events/A", "401 Unauthorized", r.text, r.status_code, "PASS" if r.status_code == 401 else "FAIL")

# Nonexistent event
try:
    r = client.get("/events/99999", headers=headers1)
    record("3. GET EVENT BY ID", "Nonexistent event", "GET /events/99999", "404 Not Found", r.text, r.status_code, "PASS" if r.status_code == 404 else "FAIL")
except Exception as e:
    record("3. GET EVENT BY ID", "Nonexistent event", "GET /events/99999", "404 Not Found", str(e), 500, "FAIL")

# ==========================================
# 4. GET EVENT TASK
# ==========================================
# Owner gets Task A
r = client.get(f"/event-tasks/{taskA_id}", headers=headers1)
record("4. GET EVENT TASK", "Task owner", "GET Task A", "200 OK", r.text, r.status_code, "PASS" if r.status_code == 200 else "FAIL")

# User 3 (Staff of Event A) attempts to access Task B (Event B) -> should be 403
r = client.get(f"/event-tasks/{taskB_id}", headers=headers3)
record("4. GET EVENT TASK", "Cross-event IDOR", "Staff of A gets Task B", "403 Forbidden", r.text, r.status_code, "FAIL" if r.status_code == 200 else "PASS")

# Nonexistent task
try:
    r = client.get("/event-tasks/99999", headers=headers1)
    record("4. GET EVENT TASK", "Nonexistent task", "GET Task 99999", "404", r.text, r.status_code, "PASS" if r.status_code == 404 else "FAIL")
except Exception as e:
    record("4. GET EVENT TASK", "Nonexistent task", "GET Task 99999", "404", str(e), 500, "FAIL")

# ==========================================
# 5. PATCH EVENT TASK
# ==========================================
# User 3 (Staff of A) updates Task B -> should be 403
r = client.patch(f"/event-tasks/{taskB_id}", json={"status": "DONE"}, headers=headers3)
record("5. PATCH EVENT TASK", "Cross-event IDOR", "Staff of A patches Task B", "403 Forbidden", r.text, r.status_code, "FAIL" if r.status_code == 200 else "PASS")

# Update only status
r = client.patch(f"/event-tasks/{taskA_id}", json={"status": "DONE"}, headers=headers1)
record("5. PATCH EVENT TASK", "Update only status", "PATCH Task A status", "200 OK", r.text, r.status_code, "PASS" if r.status_code == 200 else "FAIL")

# ==========================================
# 6. STATUS VALIDATION
# ==========================================
r = client.patch(f"/event-tasks/{taskA_id}", json={"status": "INVALID"}, headers=headers1)
record("6. STATUS VALIDATION", "Invalid status", "PATCH Task A INVALID status", "422 Unprocessable Entity", r.text, r.status_code, "PASS" if r.status_code == 422 else "FAIL")

# ==========================================
# 7. PRIORITY VALIDATION
# ==========================================
r = client.patch(f"/event-tasks/{taskA_id}", json={"priority": "URGENT"}, headers=headers1)
record("7. PRIORITY VALIDATION", "Invalid priority", "PATCH Task A URGENT priority", "422 Unprocessable Entity", r.text, r.status_code, "PASS" if r.status_code == 422 else "FAIL")

# ==========================================
# 8. AUTHORIZATION SEMANTICS
# ==========================================
r1 = client.get(f"/events/{eventA_id}")
r2 = client.get(f"/events/{eventB_id}", headers=headers1) # Owner of A trying to access B
record("8. AUTHORIZATION SEMANTICS", "Unauth vs Forbidden", "Unauth=401, Forbid=403", "401 and 403", f"r1={r1.status_code}, r2={r2.status_code}", 0, "PASS" if r1.status_code==401 and r2.status_code==403 else "FAIL")

# ==========================================
# 9. PAGINATION
# ==========================================
r = client.get(f"/events/{eventA_id}/members?page=-1&limit=0", headers=headers1)
record("9. PAGINATION", "Invalid limits", "page=-1 limit=0", "422", r.text, r.status_code, "PASS" if r.status_code == 422 else "FAIL")

# ==========================================
# Output results
# ==========================================
with open("test_results.json", "w") as f:
    json.dump(results, f, indent=2)

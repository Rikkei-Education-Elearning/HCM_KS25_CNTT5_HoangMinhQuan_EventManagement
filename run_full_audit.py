import sys
sys.stdout.reconfigure(encoding='utf-8')
import httpx
import uuid
import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.user import User
from app.models.event import Event
from app.models import EventStaff
from app.models.event_task import EventTask
from sqlalchemy import text
import jwt
import json

client = TestClient(app, raise_server_exceptions=False)
db = SessionLocal()

results = []

def rand_email():
    return f"test_{uuid.uuid4().hex[:8]}@example.com"

def record(module, test_case, input_desc, expected, response, result, note=""):
    try:
        status_code = response.status_code
        actual = response.text[:200]
    except:
        status_code = response.get("status_code", 500) if isinstance(response, dict) else 500
        actual = str(response)[:200]
        
    results.append({
        "module": module,
        "case": test_case,
        "input": input_desc,
        "expected": expected,
        "actual": actual,
        "status": status_code,
        "result": result,
        "note": note
    })
    print(f"[{result}] {module} - {test_case} (Status: {status_code})")

# A. Authentication
email1 = rand_email()
pw = "Password123"

# Register thành công
r = client.post("/auth/register", data={"email": email1, "full_name": "Test User", "password": pw})
record("Authentication", "Register thành công", "Data hợp lệ", "201 Created", r, "PASS" if r.status_code == 201 else "FAIL")

# Register thiếu dữ liệu
r = client.post("/auth/register", data={"email": rand_email()})
record("Authentication", "Register thiếu dữ liệu", "Thiếu password", "422", r, "PASS" if r.status_code == 422 else "FAIL")

# Register dữ liệu không hợp lệ (email sai)
r = client.post("/auth/register", data={"email": "invalid", "full_name": "T", "password": pw})
record("Authentication", "Register dữ liệu không hợp lệ", "Email sai format", "422/400", r, "PASS" if r.status_code in [422, 400] else "FAIL")

# Register email đã tồn tại
r = client.post("/auth/register", data={"email": email1, "full_name": "Test User 2", "password": pw})
record("Authentication", "Register email đã tồn tại", "Trùng email", "409/400", r, "PASS" if r.status_code in [409, 400] else "FAIL")

# Login thành công
r = client.post("/auth/login", data={"username": email1, "password": pw})
record("Authentication", "Login thành công", "Đúng email, pass", "200 OK", r, "PASS" if r.status_code == 200 else "FAIL")
tokens = r.json().get("data", {})
acc1 = tokens.get("access_token", "")
ref1 = tokens.get("refresh_token", "")
h1 = {"Authorization": f"Bearer {acc1}"}

# Login sai password
r = client.post("/auth/login", data={"username": email1, "password": "wrongpassword"})
record("Authentication", "Login sai password", "Sai pass", "400/401", r, "PASS" if r.status_code in [400, 401] else "FAIL")

# Login user không tồn tại
r = client.post("/auth/login", data={"username": "notexist@ex.com", "password": pw})
record("Authentication", "Login user không tồn tại", "Email chưa đk", "400/401", r, "PASS" if r.status_code in [400, 401] else "FAIL")

# Request không có authentication
r = client.get("/users/me")
record("Authentication", "Request không có authentication", "Không có token", "401", r, "PASS" if r.status_code == 401 else "FAIL")

# Token không hợp lệ
r = client.get("/users/me", headers={"Authorization": "Bearer invalid"})
record("Authentication", "Token không hợp lệ", "Token rác", "401", r, "PASS" if r.status_code == 401 else "FAIL")

# Token hết hạn
old_token = jwt.encode({"sub": email1, "exp": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)}, "1234567890", algorithm="HS256")
r = client.get("/users/me", headers={"Authorization": f"Bearer {old_token}"})
record("Authentication", "Token hết hạn", "Token cũ", "401", r, "PASS" if r.status_code == 401 else "FAIL")

# Refresh token hợp lệ
r = client.post("/auth/refresh", params={"refresh_token": ref1})
record("Authentication", "Refresh token hợp lệ", "Đúng refresh token", "200", r, "PASS" if r.status_code == 200 else "FAIL")

# Refresh token không hợp lệ (dùng access token)
r = client.post("/auth/refresh", params={"refresh_token": acc1})
record("Authentication", "Refresh token không hợp lệ", "Gửi access token", "401", r, "PASS" if r.status_code == 401 else "FAIL")

# B. User / Authorization
# Lấy thông tin user hợp lệ
r = client.get("/users/me", headers=h1)
record("User / Authorization", "Lấy thông tin user hợp lệ", "Token đúng", "200 OK", r, "PASS" if r.status_code == 200 else "FAIL")

# Truy cập khi chưa đăng nhập (test ở trên rồi, làm lại cho chắc)
r = client.get("/users/me")
record("User / Authorization", "Truy cập khi chưa đăng nhập", "Không token", "401", r, "PASS" if r.status_code == 401 else "FAIL")

# Nếu có admin-only endpoint
r = client.get("/users/", headers=h1)
record("User / Authorization", "User không đủ quyền (admin)", "User bth gọi /users/", "403/401", r, "PASS" if r.status_code in [403, 401] else "FAIL")

# Setup Event Data
email2 = rand_email()
client.post("/auth/register", data={"email": email2, "full_name": "Test 2", "password": pw})
acc2 = client.post("/auth/login", data={"username": email2, "password": pw}).json()["data"]["access_token"]
h2 = {"Authorization": f"Bearer {acc2}"}

email3 = rand_email()
client.post("/auth/register", data={"email": email3, "full_name": "Test 3", "password": pw})
acc3 = client.post("/auth/login", data={"username": email3, "password": pw}).json()["data"]["access_token"]
h3 = {"Authorization": f"Bearer {acc3}"}

u2_id = db.query(User).filter(User.email == email2).first().id
u3_id = db.query(User).filter(User.email == email3).first().id

# C. Event
# Tạo event thành công
ev_data = {"name": "Event A", "description": "D", "location": "L", "start_time": "2026-01-01T00:00:00", "end_time": "2026-01-02T00:00:00", "status": "DRAFT", "event_type": "CONFERENCE", "capacity": 100, "created_at": "2026-01-01T00:00:00"}
r = client.post("/events", data=ev_data, headers=h1)
record("Event", "Tạo event thành công", "Data hợp lệ", "201 Created", r, "PASS" if r.status_code == 201 else "FAIL")
event_id = r.json()["data"]["id"] if r.status_code == 201 else 1

# Tạo event với dữ liệu không hợp lệ
r = client.post("/events", data={"name": "No created at"}, headers=h1)
record("Event", "Tạo event với dữ liệu không hợp lệ", "Thiếu created_at", "422", r, "PASS" if r.status_code == 422 else "FAIL")

# Lấy danh sách event
r = client.get("/events", headers=h1)
record("Event", "Lấy danh sách event", "Gửi req hợp lệ", "200", r, "PASS" if r.status_code == 200 else "FAIL")

# Lấy event theo ID hợp lệ (owner)
r = client.get(f"/events/{event_id}", headers=h1)
record("Event", "Lấy event theo ID hợp lệ (owner)", "ID đúng, owner", "200", r, "PASS" if r.status_code == 200 else "FAIL")

# Lấy event theo ID hợp lệ (staff)
client.post(f"/events/{event_id}/members", data={"user_id": u2_id}, headers=h1)
r = client.get(f"/events/{event_id}", headers=h2)
record("Event", "Lấy event theo ID hợp lệ (staff)", "ID đúng, staff", "200", r, "PASS" if r.status_code == 200 else "FAIL")

# User không có quyền truy cập event (người thứ 3)
r = client.get(f"/events/{event_id}", headers=h3)
record("Event", "User không có quyền truy cập event", "Người ngoài", "403", r, "PASS" if r.status_code == 403 else "FAIL")

# Event ID không tồn tại
r = client.get("/events/99999", headers=h1)
record("Event", "Event ID không tồn tại", "ID 99999", "404", r, "PASS" if r.status_code == 404 else "FAIL")

# Update event thành công (PUT)
r = client.put(f"/events/{event_id}", data={"name": "Event A Updated", "description": "D", "location": "L", "start_time": "2026-01-01T00:00:00", "end_time": "2026-01-02T00:00:00", "status": "DRAFT", "event_type": "CONFERENCE", "capacity": 100, "created_at": "2026-01-01T00:00:00"}, headers=h1)
record("Event", "Update event thành công", "Data hợp lệ", "200", r, "PASS" if r.status_code == 200 else "FAIL")

# PATCH event
# PATCH endpoint expects JSON or Form depending on schema. The code uses `event_update: EventUpdate` which implies JSON if not wrapped in Form(...)
r = client.patch(f"/events/{event_id}", json={"name": "Patched Name"}, headers=h1)
record("Event", "PATCH event / PATCH chỉ một field", "Chỉ gửi name", "200", r, "PASS" if r.status_code == 200 else "FAIL")

# Delete/update khi không có quyền
r = client.delete(f"/events/{event_id}", headers=h3)
record("Event", "Delete khi không có quyền", "Người ngoài xoá", "403/401", r, "PASS" if r.status_code in [403, 401] else "FAIL")

# D. Event Staff / Members
# Thêm member thành công (user 3)
r = client.post(f"/events/{event_id}/members", data={"user_id": u3_id}, headers=h1)
record("Event Staff", "Thêm member/staff thành công", "User ID đúng", "201", r, "PASS" if r.status_code == 201 else "FAIL")

# Thêm member trùng
r = client.post(f"/events/{event_id}/members", data={"user_id": u3_id}, headers=h1)
record("Event Staff", "Thêm member trùng", "Add lại u3", "400", r, "PASS" if r.status_code == 400 else "FAIL")

# Member không tồn tại
r = client.post(f"/events/{event_id}/members", data={"user_id": 99999}, headers=h1)
record("Event Staff", "Thêm member không tồn tại", "ID sai", "404", r, "PASS" if r.status_code == 404 else "FAIL")

# Xem members
r = client.get(f"/events/{event_id}/members", headers=h1)
record("Event Staff", "Xem members", "Owner xem", "200", r, "PASS" if r.status_code == 200 else "FAIL")

# User không có quyền quản lý members (staff không dc remove staff?)
r = client.delete(f"/events/{event_id}/members/{u2_id}", headers=h2) # try removing self or someone else
record("Event Staff", "User không có quyền quản lý members", "Xoá không quyền", "403/401", r, "PASS" if r.status_code in [403, 401] else "FAIL")

# Remove member
r = client.delete(f"/events/{event_id}/members/{u3_id}", headers=h1)
record("Event Staff", "Remove member", "Owner xoá u3", "204", r, "PASS" if r.status_code == 204 else "FAIL")

# Remove member không tồn tại
r = client.delete(f"/events/{event_id}/members/{u3_id}", headers=h1)
record("Event Staff", "Remove member không tồn tại", "Xoá lại u3", "400/404", r, "PASS" if r.status_code in [400, 404] else "FAIL")


# E. Event Task
u1_id = db.query(User).filter(User.email == email1).first().id
# Tạo task thành công
r = client.post(f"/events/{event_id}/event-tasks", data={"event_id": event_id, "assignee_id": u1_id, "title": "T1", "description": "D", "status": "pending", "priority": "medium", "due_date": "2026-01-01T00:00:00", "created_at": "2026-01-01T00:00:00"}, headers=h1)
record("Event Task", "Tạo task thành công", "Data đúng", "201", r, "PASS" if r.status_code == 201 else "FAIL")

# Inject directly if failed so we can test further
t1 = EventTask(event_id=event_id, assignee_id=u1_id, title="T1", description="D", status="pending", priority="medium", due_date=datetime.datetime(2026, 1, 1), created_at=datetime.datetime(2026, 1, 1))
db.add(t1)
db.commit()
db.refresh(t1)
task_id = t1.id

# Tạo task với dữ liệu không hợp lệ
r = client.post(f"/events/{event_id}/event-tasks", data={"event_id": event_id}, headers=h1)
record("Event Task", "Tạo task với dữ liệu không hợp lệ", "Thiếu field", "422", r, "PASS" if r.status_code == 422 else "FAIL")

# Lấy task (owner)
r = client.get(f"/event-tasks/{task_id}", headers=h1)
record("Event Task", "Lấy task", "GET task", "200", r, "PASS" if r.status_code == 200 else "FAIL")

# Task không tồn tại
r = client.get("/event-tasks/99999", headers=h1)
record("Event Task", "Task không tồn tại", "GET 99999", "404", r, "PASS" if r.status_code == 404 else "FAIL")

# Update task / PATCH chỉ một field
r = client.patch(f"/event-tasks/{task_id}", json={"title": "New Title"}, headers=h1)
record("Event Task", "PATCH chỉ một field", "Chỉ gửi title", "200", r, "PASS" if r.status_code == 200 else "FAIL")

# Delete task
r = client.delete(f"/event-tasks/{task_id}", headers=h1)
record("Event Task", "Delete task", "Xoá task hợp lệ", "200/204", r, "PASS" if r.status_code in [200, 204] else "FAIL")

# F. Status và Priority
# Recreate task
t2 = EventTask(event_id=event_id, assignee_id=u1_id, title="T2", description="D", status="pending", priority="medium", due_date=datetime.datetime(2026, 1, 1), created_at=datetime.datetime(2026, 1, 1))
db.add(t2)
db.commit()
db.refresh(t2)
t2_id = t2.id

# Status
for stat in ["TODO", "pending", "in_progress", "completed", "DONE", "INVALID"]:
    r = client.patch(f"/event-tasks/{t2_id}", json={"status": stat}, headers=h1)
    if r.status_code == 422:
        record("Status và Priority", f"Status - {stat}", "Patch status", "Validation error expected for some", r, "PASS" if stat not in ["pending", "in_progress", "completed"] else "FAIL")
    elif r.status_code == 200:
        record("Status và Priority", f"Status - {stat}", "Patch status", "Success expected for valid", r, "PASS" if stat in ["pending", "in_progress", "completed"] else "FAIL")
    else:
        record("Status và Priority", f"Status - {stat}", "Patch status", "200/422", r, "FAIL")

# Priority
for prio in ["LOW", "low", "medium", "high", "URGENT", "INVALID"]:
    r = client.patch(f"/event-tasks/{t2_id}", json={"priority": prio}, headers=h1)
    if r.status_code == 422:
        record("Status và Priority", f"Priority - {prio}", "Patch priority", "Validation error expected for some", r, "PASS" if prio not in ["low", "medium", "high"] else "FAIL")
    elif r.status_code == 200:
        record("Status và Priority", f"Priority - {prio}", "Patch priority", "Success expected for valid", r, "PASS" if prio in ["low", "medium", "high"] else "FAIL")
    else:
        record("Status và Priority", f"Priority - {prio}", "Patch priority", "200/422", r, "FAIL")

# G. Pagination
# Limit & page
r = client.get(f"/events/{event_id}/members?page=1&limit=5", headers=h1)
record("Pagination", "page=1, limit hợp lệ", "GET members", "200", r, "PASS" if r.status_code == 200 else "FAIL")
r = client.get(f"/events/{event_id}/members?page=0&limit=5", headers=h1)
record("Pagination", "page=0", "GET members", "422", r, "PASS" if r.status_code == 422 else "FAIL")
r = client.get(f"/events/{event_id}/members?page=-1&limit=5", headers=h1)
record("Pagination", "page âm", "GET members", "422", r, "PASS" if r.status_code == 422 else "FAIL")
r = client.get(f"/events/{event_id}/members?page=1&limit=0", headers=h1)
record("Pagination", "limit=0", "GET members", "422", r, "PASS" if r.status_code == 422 else "FAIL")
r = client.get(f"/events/{event_id}/members?page=1&limit=-1", headers=h1)
record("Pagination", "limit âm", "GET members", "422", r, "PASS" if r.status_code == 422 else "FAIL")
r = client.get(f"/events/{event_id}/members?page=999&limit=5", headers=h1)
record("Pagination", "page vượt quá số trang", "GET members", "200", r, "PASS" if r.status_code == 200 else "FAIL")

# Delete Event (To clean up and test delete event)
r = client.delete(f"/events/{event_id}", headers=h1)
record("Event", "Delete event thành công", "Xoá event", "204", r, "PASS" if r.status_code == 204 else "FAIL")
r = client.delete(f"/events/{event_id}", headers=h1)
record("Event", "Delete event không tồn tại", "Xoá event đã xoá", "404", r, "PASS" if r.status_code == 404 else "FAIL")

with open("full_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("Done!")

# Event Management API

Dự án quản lý sự kiện xây dựng với **FastAPI**, **SQLAlchemy** và **Pydantic**.

## Cấu trúc thư mục

```
app/
├── main.py              # Khởi tạo FastAPI app, include routers, middleware
├── core/                # Cấu hình dùng chung
│   ├── config.py        # Đọc biến môi trường và settings
│   └── security.py      # Hash password, JWT encode/decode
├── db/                  # Kết nối và session database
│   └── database.py      # engine, SessionLocal, Base, get_db
├── models/              # SQLAlchemy models
│   ├── user.py
│   ├── event.py         # Event, EventStaff
│   └── event_task.py
├── schemas/             # Pydantic request/response schemas
├── routers/             # FastAPI APIRouter theo module
│   ├── auth.py          # Register/Login
│   ├── users.py         # User endpoints
│   ├── event.py         # Sự kiện/Member endpoints
│   └── event_task.py    # Công việc sự kiện endpoints
├── services/            # Nghiệp vụ và thao tác dữ liệu
├── dependencies/        # get_current_user, role/permission dependencies
└── utils/               # Helper dùng chung
tests/                   # Test API/service
.env.example             # Mẫu biến môi trường
requirements.txt         # Danh sách thư viện
```

## Cài đặt

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

## Chạy ứng dụng

```bash
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

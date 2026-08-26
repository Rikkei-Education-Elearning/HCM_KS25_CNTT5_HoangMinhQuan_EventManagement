# API Test Checklist

**Project:** FastAPI Backend (HCM_KS25_CNTT5_HoangMinhQuan_EventManagement)

## 1. Test Summary

- **Total test cases:** 58
- **PASS:** 53
- **FAIL:** 5
- **BLOCKED:** 0
- **NOT TESTED:** 0

## 2. Detailed Test Results

| # | Module | Endpoint | Test case | Input | Expected result | Actual result | Status |
|---|---|---|---|---|---|---|---|
| 1 | Authentication | API Endpoint | Register thành công | Data hợp lệ | 201 Created | {"statusCode":201,"message":"User created successfully","data":{"id":44,"emai... | **PASS** |
| 2 | Authentication | API Endpoint | Register thiếu dữ liệu | Thiếu password | 422 | {"detail":[{"type":"missing","loc":["body","password"],"msg":"Field required"... | **PASS** |
| 3 | Authentication | API Endpoint | Register dữ liệu không hợp lệ | Email sai format | 422/400 | {"statusCode":400,"message":"Email already exists","data":null,"error":"Email... | **PASS** |
| 4 | Authentication | API Endpoint | Register email đã tồn tại | Trùng email | 409/400 | {"statusCode":400,"message":"Email already exists","data":null,"error":"Email... | **PASS** |
| 5 | Authentication | API Endpoint | Login thành công | Đúng email, pass | 200 OK | {"statusCode":200,"message":"Login successful","data":{"access_token":"eyJhbG... | **PASS** |
| 6 | Authentication | API Endpoint | Login sai password | Sai pass | 400/401 | {"statusCode":400,"message":"Invalid password or email","data":null,"error":"... | **PASS** |
| 7 | Authentication | API Endpoint | Login user không tồn tại | Email chưa đk | 400/401 | {"statusCode":400,"message":"Invalid password or email","data":null,"error":"... | **PASS** |
| 8 | Authentication | API Endpoint | Request không có authentication | Không có token | 401 | {"detail":"Not authenticated"} | **PASS** |
| 9 | Authentication | API Endpoint | Token không hợp lệ | Token rác | 401 | {"statusCode":401,"message":"Token invalid","data":null,"error":"Token invali... | **PASS** |
| 10 | Authentication | API Endpoint | Token hết hạn | Token cũ | 401 | {"statusCode":401,"message":"Token expired","data":null,"error":"Token expire... | **PASS** |
| 11 | Authentication | API Endpoint | Refresh token hợp lệ | Đúng refresh token | 200 | {"statusCode":401,"message":"Unauthorized","data":null,"error":"Unauthorized"... | **FAIL** |
| 12 | Authentication | API Endpoint | Refresh token không hợp lệ | Gửi access token | 401 | {"statusCode":401,"message":"Unauthorized","data":null,"error":"Unauthorized"... | **PASS** |
| 13 | User / Authorization | API Endpoint | Lấy thông tin user hợp lệ | Token đúng | 200 OK | {"statusCode":200,"message":"User retrieved successfully","data":{"id":44,"em... | **PASS** |
| 14 | User / Authorization | API Endpoint | Truy cập khi chưa đăng nhập | Không token | 401 | {"detail":"Not authenticated"} | **PASS** |
| 15 | User / Authorization | API Endpoint | User không đủ quyền (admin) | User bth gọi /users/ | 403/401 | {"statusCode":403,"message":"Forbidden","data":null,"error":"Forbidden","time... | **PASS** |
| 16 | Event | API Endpoint | Tạo event thành công | Data hợp lệ | 201 Created | {"statusCode":201,"message":"Event created successfully","data":{"id":27,"nam... | **PASS** |
| 17 | Event | API Endpoint | Tạo event với dữ liệu không hợp lệ | Thiếu created_at | 422 | {"statusCode":201,"message":"Event created successfully","data":{"id":28,"nam... | **FAIL** |
| 18 | Event | API Endpoint | Lấy danh sách event | Gửi req hợp lệ | 200 | {"statusCode":200,"message":"Event found","data":{"id":27,"name":"Event A","d... | **PASS** |
| 19 | Event | API Endpoint | Lấy event theo ID hợp lệ (owner) | ID đúng, owner | 200 | {"statusCode":200,"message":"Event found","data":{"id":27,"name":"Event A","d... | **PASS** |
| 20 | Event | API Endpoint | Lấy event theo ID hợp lệ (staff) | ID đúng, staff | 200 | {"statusCode":200,"message":"Event found","data":{"id":27,"name":"Event A","d... | **PASS** |
| 21 | Event | API Endpoint | User không có quyền truy cập event | Người ngoài | 403 | {"statusCode":401,"message":"User not authorized to access this event","data"... | **FAIL** |
| 22 | Event | API Endpoint | Event ID không tồn tại | ID 99999 | 404 | {"statusCode":404,"message":"Event not found","data":null,"error":"Event not ... | **PASS** |
| 23 | Event | API Endpoint | Update event thành công | Data hợp lệ | 200 | {"statusCode":200,"message":"Event updated","data":{"id":27,"name":"Event A U... | **PASS** |
| 24 | Event | API Endpoint | PATCH event / PATCH chỉ một field | Chỉ gửi name | 200 | {"statusCode":200,"message":"Event patched","data":{"id":27,"name":"Patched N... | **PASS** |
| 25 | Event | API Endpoint | Delete khi không có quyền | Người ngoài xoá | 403/401 | {"statusCode":401,"message":"User not authorized to delete this event","data"... | **PASS** |
| 26 | Event Staff | API Endpoint | Thêm member/staff thành công | User ID đúng | 201 | {"statusCode":201,"message":"Member added to event","data":{"id":27,"name":"P... | **PASS** |
| 27 | Event Staff | API Endpoint | Thêm member trùng | Add lại u3 | 400 | {"statusCode":400,"message":"User is already a member of this event","data":n... | **PASS** |
| 28 | Event Staff | API Endpoint | Thêm member không tồn tại | ID sai | 404 | {"statusCode":404,"message":"User not found","data":null,"error":"User not fo... | **PASS** |
| 29 | Event Staff | API Endpoint | Xem members | Owner xem | 200 | {"statusCode":200,"message":"Members retrieved successfully","data":[{"id":45... | **PASS** |
| 30 | Event Staff | API Endpoint | User không có quyền quản lý members | Xoá không quyền | 403/401 | {"statusCode":401,"message":"User not authorized to remove members from this ... | **PASS** |
| 31 | Event Staff | API Endpoint | Remove member | Owner xoá u3 | 204 |  | **PASS** |
| 32 | Event Staff | API Endpoint | Remove member không tồn tại | Xoá lại u3 | 400/404 | {"statusCode":400,"message":"User is not a member of this event","data":null,... | **PASS** |
| 33 | Event Task | API Endpoint | Tạo task thành công | Data đúng | 201 | {"statusCode":201,"message":"Event task created successfully","data":{"id":17... | **PASS** |
| 34 | Event Task | API Endpoint | Tạo task với dữ liệu không hợp lệ | Thiếu field | 422 | {"detail":[{"type":"missing","loc":["body","title"],"msg":"Field required","i... | **PASS** |
| 35 | Event Task | API Endpoint | Lấy task | GET task | 200 | {"statusCode":200,"message":"Event Task found","data":{"id":18,"event_id":27,... | **PASS** |
| 36 | Event Task | API Endpoint | Task không tồn tại | GET 99999 | 404 | {"statusCode":404,"message":"Event Task not found","data":null,"error":"Event... | **PASS** |
| 37 | Event Task | API Endpoint | PATCH chỉ một field | Chỉ gửi title | 200 | {"statusCode":200,"message":"Event Task updated","data":{"id":18,"event_id":2... | **PASS** |
| 38 | Event Task | API Endpoint | Delete task | Xoá task hợp lệ | 200/204 | {"statusCode":200,"message":"Event Task deleted","data":{"id":18,"event_id":2... | **PASS** |
| 39 | Status và Priority | API Endpoint | Status - TODO | Patch status | Validation error expected for some | {"detail":[{"type":"enum","loc":["body","status"],"msg":"Input should be 'pen... | **PASS** |
| 40 | Status và Priority | API Endpoint | Status - pending | Patch status | Success expected for valid | {"statusCode":200,"message":"Event Task updated","data":{"id":19,"event_id":2... | **PASS** |
| 41 | Status và Priority | API Endpoint | Status - in_progress | Patch status | Success expected for valid | {"statusCode":200,"message":"Event Task updated","data":{"id":19,"event_id":2... | **PASS** |
| 42 | Status và Priority | API Endpoint | Status - completed | Patch status | Success expected for valid | {"statusCode":200,"message":"Event Task updated","data":{"id":19,"event_id":2... | **PASS** |
| 43 | Status và Priority | API Endpoint | Status - DONE | Patch status | Validation error expected for some | {"detail":[{"type":"enum","loc":["body","status"],"msg":"Input should be 'pen... | **PASS** |
| 44 | Status và Priority | API Endpoint | Status - INVALID | Patch status | Validation error expected for some | {"detail":[{"type":"enum","loc":["body","status"],"msg":"Input should be 'pen... | **PASS** |
| 45 | Status và Priority | API Endpoint | Priority - LOW | Patch priority | Validation error expected for some | {"detail":[{"type":"enum","loc":["body","priority"],"msg":"Input should be 'l... | **PASS** |
| 46 | Status và Priority | API Endpoint | Priority - low | Patch priority | Success expected for valid | {"statusCode":200,"message":"Event Task updated","data":{"id":19,"event_id":2... | **PASS** |
| 47 | Status và Priority | API Endpoint | Priority - medium | Patch priority | Success expected for valid | {"statusCode":200,"message":"Event Task updated","data":{"id":19,"event_id":2... | **PASS** |
| 48 | Status và Priority | API Endpoint | Priority - high | Patch priority | Success expected for valid | {"statusCode":200,"message":"Event Task updated","data":{"id":19,"event_id":2... | **PASS** |
| 49 | Status và Priority | API Endpoint | Priority - URGENT | Patch priority | Validation error expected for some | {"detail":[{"type":"enum","loc":["body","priority"],"msg":"Input should be 'l... | **PASS** |
| 50 | Status và Priority | API Endpoint | Priority - INVALID | Patch priority | Validation error expected for some | {"detail":[{"type":"enum","loc":["body","priority"],"msg":"Input should be 'l... | **PASS** |
| 51 | Pagination | API Endpoint | page=1, limit hợp lệ | GET members | 200 | {"statusCode":200,"message":"Members retrieved successfully","data":[{"id":45... | **PASS** |
| 52 | Pagination | API Endpoint | page=0 | GET members | 422 | {"detail":[{"type":"greater_than_equal","loc":["query","page"],"msg":"Input s... | **PASS** |
| 53 | Pagination | API Endpoint | page âm | GET members | 422 | {"detail":[{"type":"greater_than_equal","loc":["query","page"],"msg":"Input s... | **PASS** |
| 54 | Pagination | API Endpoint | limit=0 | GET members | 422 | {"detail":[{"type":"greater_than_equal","loc":["query","limit"],"msg":"Input ... | **PASS** |
| 55 | Pagination | API Endpoint | limit âm | GET members | 422 | {"detail":[{"type":"greater_than_equal","loc":["query","limit"],"msg":"Input ... | **PASS** |
| 56 | Pagination | API Endpoint | page vượt quá số trang | GET members | 200 | {"statusCode":200,"message":"Members retrieved successfully","data":[],"error... | **PASS** |
| 57 | Event | API Endpoint | Delete event thành công | Xoá event | 204 | Internal Server Error | **FAIL** |
| 58 | Event | API Endpoint | Delete event không tồn tại | Xoá event đã xoá | 404 | Internal Server Error | **FAIL** |

## 3. Failed Cases


### Authentication - Refresh token hợp lệ
- **Endpoint:** Authentication API
- **Test case:** Refresh token hợp lệ
- **Request:** Đúng refresh token
- **Expected:** 200
- **Actual:** {"statusCode":401,"message":"Unauthorized","data":null,"error":"Unauthorized","timestamp":"2026-08-26T15:17:39.128681","path":"/auth/refresh"}
- **HTTP status:** 401
- **Error/bug:** Lỗi logic hoặc crash

### Event - Tạo event với dữ liệu không hợp lệ
- **Endpoint:** Event API
- **Test case:** Tạo event với dữ liệu không hợp lệ
- **Request:** Thiếu created_at
- **Expected:** 422
- **Actual:** {"statusCode":201,"message":"Event created successfully","data":{"id":28,"name":"No created at","description":null,"owner_id":44,"created_at":"2026-08-26T15:17:40"},"error":null,"timestamp":"2026-08-2
- **HTTP status:** 201
- **Error/bug:** Lỗi logic hoặc crash

### Event - User không có quyền truy cập event
- **Endpoint:** Event API
- **Test case:** User không có quyền truy cập event
- **Request:** Người ngoài
- **Expected:** 403
- **Actual:** {"statusCode":401,"message":"User not authorized to access this event","data":null,"error":"User not authorized to access this event","timestamp":"2026-08-26T15:17:40.278754","path":"/events/27"}
- **HTTP status:** 401
- **Error/bug:** Lỗi logic hoặc crash

### Event - Delete event thành công
- **Endpoint:** Event API
- **Test case:** Delete event thành công
- **Request:** Xoá event
- **Expected:** 204
- **Actual:** Internal Server Error
- **HTTP status:** 500
- **Error/bug:** Lỗi logic hoặc crash

### Event - Delete event không tồn tại
- **Endpoint:** Event API
- **Test case:** Delete event không tồn tại
- **Request:** Xoá event đã xoá
- **Expected:** 404
- **Actual:** Internal Server Error
- **HTTP status:** 500
- **Error/bug:** Lỗi logic hoặc crash

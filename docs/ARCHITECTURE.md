# Kiến trúc hệ thống — ROVVA

**Dự án:** ROVVA Smart Stay Platform  
**Kiến trúc:** Server-Side Rendering (Flask + Jinja2 + SQLite)  
**Cập nhật:** 12/07/2026 — bám sát codebase

---

## Technology stack

| Thành phần | Công nghệ |
|------------|-----------|
| Runtime | Python 3.10+ |
| Web framework | Flask 3, Flask-Login, Flask-SQLAlchemy |
| Database | SQLite — `instance/rova_host.db` |
| Frontend | HTML5, Bootstrap 5.3.8, Jinja2, Vanilla JS |
| AI / Analytics | scikit-learn + pandas (Smart Match); Groq API (AI chat) |
| Password | Werkzeug hash |

**Dependencies:** `requirements.txt` — Flask, Flask-SQLAlchemy, Flask-Login, python-dotenv, pandas, scikit-learn, numpy.

---

## Cấu trúc repository

```text
ROVVA/
├── backend/app/
│   ├── __init__.py          # create_app(): DB, seed, patch, template globals
│   ├── config.py            # Dev/Prod, DATABASE_URL, GROQ_*
│   ├── extensions.py        # db, login_manager
│   ├── models/              # 13 ORM models
│   ├── routes/
│   │   ├── auth/            # login, register, logout, verify, forgot/reset
│   │   ├── customer/        # main.py, booking.py
│   │   ├── host/            # 9 blueprints + copilot.py (chưa register)
│   │   └── admin/           # portal SPA
│   ├── services/
│   │   ├── smart_match.py
│   │   ├── ai_chat.py
│   │   ├── customer_messages.py
│   │   ├── member_tier.py
│   │   ├── booking_notify.py
│   │   ├── host_dashboard.py, host_report.py
│   │   ├── admin_dashboard.py, admin_portal.py
│   │   └── host_copilot/    # trợ lý vận hành: persona, maintenance, revenue (giả lập ML)
│   ├── utils/               # media, accommodation_display, host_display, reviews
│   ├── data/blog_posts.py   # Nội dung blog marketing
│   └── seed.py
├── frontend/
│   ├── templates/           # customer, host, admin, auth
│   └── static/              # customer/, host/, admin/, shared/
├── scripts/fill_accommodation_images.py
├── docs/
├── instance/                # SQLite (gitignored)
├── .env.example
└── run.py                   # Entry point: create_app(), port 5000
```

---

## Application factory

`create_app()` trong `backend/app/__init__.py`:

1. Load `.env` từ thư mục gốc (không ghi đè biến môi trường đã có).
2. Khởi tạo SQLAlchemy + Flask-Login.
3. `register_blueprints(app)` — xem bảng dưới.
4. `db.create_all()` + patch schema (`patch_conversation_schema`, `patch_review_schema`, …).
5. Seed nếu DB trống (`seed_database()`).
6. Inject Jinja globals: `format_vnd`, `format_stay_range`, media helpers.

**Route gốc `/`:** redirect theo `current_user.role` — `admin` → `/admin/`, `host` → `/host/`, còn lại → `/customer/`.

---

## Blueprints đã register

File: `backend/app/routes/__init__.py`

| Blueprint | URL prefix đăng ký | Blueprint prefix nội bộ | Ví dụ URL |
|-----------|-------------------|-------------------------|-----------|
| `auth_bp` | (không) | — | `/login`, `/register`, `/logout` |
| `customer_bp` | `/customer` | — | `/customer/`, `/customer/search` |
| `customer_booking_bp` | `/customer/booking` | — | `/customer/booking/checkout/<code>` |
| `main_bp` (host) | `/host` | — | `/host/`, `/host/profile` |
| `accommodation_bp` | `/host/accommodation` | `/accommodations` | `/host/accommodation/accommodations/` |
| `booking_bp` | `/host/booking` | `/bookings` | `/host/booking/bookings/` |
| `payment_bp` | `/host/payment` | `/payments` | `/host/payment/payments/` |
| `dispute_bp` | `/host/dispute` | `/disputes` | `/host/dispute/disputes/` |
| `message_bp` | `/host/message` | `/messages` | `/host/message/messages/` |
| `promotion_bp` | `/host/promotion` | `/promotions` | `/host/promotion/promotions/` |
| `report_bp` | `/host/report` | `/reports` | `/host/report/reports/` |
| `support_bp` | `/host/support` | — | `/host/support/faq` |
| `admin_bp` | `/admin` | — | `/admin/` |

**Chưa register:** blueprint trang trợ lý vận hành (`copilot.py`) — nếu bật sẽ có `/host/copilot/`.

---

## Luồng request

```text
HTTP Request
  → Flask blueprint routing
  → Flask-Login (session cookie → current_user)
  → @login_required / @admin_required (nếu có)
  → Route handler
  → Service layer (tùy chức năng) hoặc SQLAlchemy ORM
  → render_template() → Jinja2 HTML
  → HTTP Response
```

---

## Luồng đặt phòng (Customer)

Hằng số: `HOLD_MINUTES = 20` trong `backend/app/routes/customer/booking.py`.

```text
GET /customer/search hoặc /customer/smart-search
  → GET /customer/accommodation/<id>
  → POST /customer/booking/create/<room_id>
       • Kiểm tra overlap với booking status confirmed + holding
       • Homestay/Villa: chặn toàn bộ phòng trong CSLT
       • Tạo Booking: status=holding, hold_expiry_at = now + 20 phút
  → GET/POST /customer/booking/checkout/<code>
       • Tính giá: phòng × đêm + dịch vụ − promo − xu (50.000đ nếu tick)
       • Tiền mặt → status=confirmed, payment_status=pending, commission 15%
       • Online → redirect /customer/booking/payment/online/<code>
  → [Online] POST confirm → payment-callback?status=success
       → status=confirmed, payment_status=paid, payment_gateway_ref
  → GET /customer/booking/order/<code>
```

**Khách vãng lai:** `guest_id=NULL`; quyền truy cập đơn qua `session["anonymous_booking_codes"]`.

**Hết hạn giữ chỗ:** Hủy lazy khi truy cập checkout/payment hoặc kiểm tra overlap — **không có** cron/background job.

**Email xác nhận:** `booking_notify.send_booking_confirmation_email()` — chỉ log, không SMTP.

---

## Services layer

### Smart Match (`services/smart_match.py`)
- Đọc `rooms` + `accommodations` từ SQLite (pandas).
- TF-IDF vectorize corpus mô tả; cosine similarity blend rating (85% + 15%).
- Route: `GET /customer/smart-search?q=...` — top 6 phòng kèm `reasons`.

### AI Chat (`services/ai_chat.py`)
- Groq OpenAI-compatible API; model mặc định `llama-3.3-70b-versatile`.
- Customer: `POST /customer/booking/api/ai-chat`.
- Host: `POST /host/api/ai-chat` (system prompt riêng).
- Cần `GROQ_API_KEY` trong `.env`.

### Customer messages (`services/customer_messages.py`)
- CRUD hội thoại guest ↔ host; `get_or_create_host_conversation()` cho "Liên hệ ngay".

### Member tier (`services/member_tier.py`)
- Hạng thành viên từ tổng chi tiêu booking `completed` trong 365 ngày.
- Hiển thị tại `/customer/account/tier`; **chưa** áp dụng % giảm giá theo tier ở checkout.

### Trợ lý vận hành thông minh (`services/host_copilot/`)

| Module | Chức năng |
|--------|-----------|
| `persona.py` | Suy luận chân dung khách từ booking (rule-based) |
| `maintenance.py` | Radar cảnh báo bảo trì — quét review/message, từ khóa |
| `revenue.py` | Gợi ý tối ưu giá bán và doanh thu — **thiết kế dùng ML**; hiện `build_recommendations()` **giả lập** theo occupancy, chưa gọi mô hình học máy |
| `context.py` | Gom metrics host |

Dashboard host (`/host/`) nhúng gợi ý từ `build_recommendations()`. Trang module riêng (`host/copilot/index.html`) chưa kết nối route (blueprint chưa register).

### Admin portal (`services/admin_portal.py`)
- `build_portal_context()` — serialize toàn bộ data cho SPA `admin/portal.html`.

### Booking notify (`services/booking_notify.py`)
- Mock gửi email — ghi log console.

---

## Media & static files

Ảnh **không** lưu BLOB trong DB. Quy ước:

| Loại | Path |
|------|------|
| Cover CSLT | `frontend/static/customer/images/accommodations/<acc_id>/cover.jpg` |
| Ảnh phòng | `.../accommodations/<acc_id>/rooms/<room_id>.jpg` |
| Avatar | `frontend/static/customer/images/avatars/<user_id>.jpg` |
| QR thanh toán | `frontend/static/customer/images/payment/qr-vietinbank.png` |
| Placeholder | `frontend/static/customer/images/placeholders/*.svg` |

Helper `utils/media.py` → `resolve_media()` fallback SVG. Chi tiết: [HUONG_DAN_ANH_DEMO.md](HUONG_DAN_ANH_DEMO.md).

---

## Database

**13 bảng** — chi tiết [ERD.md](ERD.md).

| Khởi tạo | Mô tả |
|----------|-------|
| `py -m flask --app run seed` | Drop all + create + insert demo |
| App startup | `create_all()` + patch + seed nếu trống |

**Seed demo:** 12 CSLT, 32 phòng, 14 booking, 3 promotion, 3 dispute, 3 conversation, 4 wallet transaction (guest ~192 xu), 3 favorite.

**Patch khi startup:** `patch_review_schema`, `patch_admin_schema`, `patch_conversation_schema`, `patch_guest_messages_demo`, `patch_host_payment_demo`, `patch_guest_review_demo`, `patch_host_notifications_demo`, `patch_host_notifications_links`, `patch_host_id_card_demo`, `patch_guest_insight_demo`.

---

## Phân quyền (RBAC)

| `users.role` | Quyền |
|--------------|-------|
| `guest` | Customer portal — tìm, đặt, tài khoản |
| `host` | Host portal — CSLT/booking của mình |
| `admin` | Admin portal — toàn hệ thống |

`users.admin_role` (chỉ admin): `super`, `admin`, `support` — UI portal có phân biệt; route chưa siết chi tiết theo `admin_role`.

**Lưu ý:** Nhiều route host chỉ `@login_required`, **chưa** kiểm tra `role == "host"`.

---

## Frontend templates

| Khu vực | Số file | Entry chính |
|---------|---------|-------------|
| Customer | 71 | `customer/base.html` |
| Host | 43 | `host/layout/base.html` |
| Admin | 24 | `admin/portal.html` (SPA) |
| Auth | 6 | `auth/login.html`, `auth/register.html` |

**Template thiếu (route có, file không):**
- `customer/pages/host_registration.html` — `/customer/become-host`
- `auth/forgot_password.html` — `/forgot-password`
- `auth/reset_password.html` — `/reset-password/<token>`

**Template legacy:** payment step1–3, trip detail/cancel, hotel-guest.html, … — không nằm trong luồng route chính.

---

## Triển khai dev

```powershell
pip install -r requirements.txt
py -m flask --app run seed
py run.py
```

**Production (chưa):** PostgreSQL, Redis session, HTTPS, WSGI (gunicorn).

---

## Tài liệu liên quan

- [ERD.md](ERD.md)
- [SRS.md](SRS.md)
- [BAO_CAO_SRS.md](BAO_CAO_SRS.md)
- [ManHinh.md](ManHinh.md)
- [HUONG_DAN_ANH_DEMO.md](HUONG_DAN_ANH_DEMO.md)

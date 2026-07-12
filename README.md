# ROVVA — Smart Stay Platform

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/flask-3.x-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-Educational-orange.svg)]()

> Nền tảng đặt phòng homestay và khách sạn thông minh trên Flask SSR, phục vụ 3 vai trò: **Customer**, **Host**, **Admin**.

**Cập nhật tài liệu:** 12/07/2026 — đồng bộ với codebase hiện tại.

---

## Tính năng chính

### Customer
- **Smart Match:** TF-IDF + cosine similarity — tìm phòng bằng câu tiếng Việt tự nhiên (`/customer/smart-search`).
- **Đặt phòng:** Tìm kiếm → chi tiết CSLT → giữ chỗ **20 phút** → checkout → thanh toán **tiền mặt** hoặc **online QR** (mô phỏng VietinBank).
- **Tài khoản:** Profile, chuyến đi, ví xu, hạng thành viên, yêu thích, đánh giá, tin nhắn host, bảo mật.
- **AI Chat:** Trợ lý Groq (`/customer/chat`) — cần `GROQ_API_KEY`.
- **Khách vãng lai:** Đặt phòng không cần đăng nhập; truy cập đơn qua session `anonymous_booking_codes`.

### Host
- Dashboard, CRUD cơ sở lưu trú (CSLT) và phòng, booking, khuyến mãi, báo cáo.
- Thanh toán & rút tiền, tranh chấp, tin nhắn khách, thông báo (UI).
- **Trợ lý vận hành thông minh:** phân tích chân dung khách, radar cảnh báo bảo trì, gợi ý tối ưu giá bán và doanh thu — hiển thị trên dashboard; trang module riêng chưa kết nối route.
- **Gợi ý giá & doanh thu:** thiết kế dùng mô hình máy học; hiện tại **chưa tích hợp ML** — chỉ giả lập bằng rule engine từ dữ liệu occupancy.
- AI chat vận hành (`/host/ai-chat`).

### Admin
- Portal SPA một trang (`/admin/`) — 9 module: dashboard, users, hosts, rooms, bookings, disputes, payments, promotions, admins.

---

## Tech stack

| Thành phần | Công nghệ |
|------------|-----------|
| Backend | Python 3.10+, Flask 3, Flask-Login, Flask-SQLAlchemy |
| Database | SQLite — `instance/rova_host.db` (13 bảng) |
| Frontend | HTML5, Bootstrap 5.3.8, Jinja2, Vanilla JS |
| AI / Data | pandas, scikit-learn (Smart Match); Groq API (AI chat) |

---

## Cài đặt & chạy

### Yêu cầu
- Python 3.10+
- pip

### Các bước

```powershell
git clone https://github.com/LeGiaVan/ROVVA.git
cd ROVVA
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
py -m flask --app run seed
py run.py
```

Truy cập: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Biến môi trường (tùy chọn)

Sao chép `.env.example` thành `.env`:

```env
SECRET_KEY=dev-rova-host-secret
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## Tài khoản demo

| Vai trò | Email | Mật khẩu | Sau login |
|---------|-------|----------|-----------|
| Customer | `1@ss` | `1` | `/customer/` |
| Host | `van.quangia@rova.vn` | `password123` | `/host/` |
| Admin | `admin@rova.vn` | `admin123` | `/admin/` |
| Host chờ duyệt | `host.pending@rova.vn` | `123456` | Duyệt tại Admin |

---

## Routes chính

| Chức năng | URL |
|-----------|-----|
| Trang gốc (redirect theo role) | `/` |
| Đăng nhập / đăng ký | `/login`, `/register` |
| Customer hub | `/customer/` |
| Tìm kiếm | `/customer/search` |
| Smart Match | `/customer/smart-search` |
| Chi tiết CSLT | `/customer/accommodation/<id>` |
| Tạo booking | `POST /customer/booking/create/<room_id>` |
| Checkout | `/customer/booking/checkout/<code>` |
| Thanh toán online | `/customer/booking/payment/online/<code>` |
| Chi tiết đơn | `/customer/booking/order/<code>` |
| Chuyến đi | `/customer/trips` |
| AI chat | `/customer/chat` |
| Host dashboard | `/host/` |
| Host CSLT | `/host/accommodation/accommodations/` |
| Host booking | `/host/booking/bookings/` |
| Host tin nhắn | `/host/message/messages/` |
| Admin portal | `/admin/` |

---

## Cấu trúc dự án

```text
ROVVA/
├── backend/app/
│   ├── models/          # 13 ORM models
│   ├── routes/          # auth, customer, host (9 module), admin
│   ├── services/        # smart_match, ai_chat, host_copilot, …
│   ├── utils/           # media, display helpers
│   └── seed.py          # Dữ liệu demo + patch schema
├── frontend/
│   ├── templates/       # 144 HTML (customer 71, host 43, admin 24, auth 6)
│   └── static/          # CSS, JS, images
├── docs/                # Tài liệu dự án
├── scripts/             # fill_accommodation_images.py
├── instance/            # SQLite (tạo khi chạy)
├── requirements.txt
└── run.py
```

---

## Hạn chế đã biết (demo)

| Hạng mục | Trạng thái |
|----------|------------|
| Payment gateway / SMTP | Mô phỏng |
| `/customer/become-host` | Template `host_registration.html` thiếu → 404 |
| `/forgot-password`, `/reset-password` | Template thiếu → 404 |
| Trang trợ lý vận hành thông minh | Module riêng chưa kết nối route |
| Gợi ý giá & doanh thu (ML) | Chưa tích hợp mô hình — đang giả lập |
| Ví xu tại checkout | Giảm giá UI, chưa trừ `wallet_transactions` |
| Promotion host | Chưa dùng ở checkout (mã cứng `WELCOME10`, `ROVVA50`) |
| Hủy booking / check-in-out | Chưa có route customer |
| Automated tests | Chưa có |

Chi tiết: [docs/BAO_CAO_SRS.md](docs/BAO_CAO_SRS.md).

---

## Tài liệu

| Tài liệu | Mô tả |
|----------|-------|
| [SRS.md](docs/SRS.md) | Đặc tả yêu cầu + quy trình nghiệp vụ |
| [ERD.md](docs/ERD.md) | Sơ đồ 13 bảng SQLite |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Kiến trúc, blueprints, luồng đặt phòng |
| [BAO_CAO_SRS.md](docs/BAO_CAO_SRS.md) | Đối chiếu SRS ↔ codebase |
| [ManHinh.md](docs/ManHinh.md) | Mô tả từng màn hình & luồng stakeholder |
| [VietBai.md](docs/VietBai.md) | Nội dung viết bài đồ án |
| [HUONG_DAN_ANH_DEMO.md](docs/HUONG_DAN_ANH_DEMO.md) | Quy ước ảnh & script fill |

---

## License

Dự án phục vụ mục đích học tập, nghiên cứu và thử nghiệm công nghệ.

# Tài liệu đặc tả yêu cầu hệ thống (SRS) — ROVVA

> Đặc tả yêu cầu cho nền tảng đặt phòng homestay/khách sạn đa vai trò (Customer, Host, Admin).  
> **Cập nhật:** 12/07/2026 — mục 4 mô tả **triển khai thực tế** trong codebase; đối chiếu chi tiết tại [BAO_CAO_SRS.md](BAO_CAO_SRS.md).

---

## 1. Yêu cầu phi chức năng (NFR)

| Mã | Hạng mục | Mô tả | Ưu tiên |
|----|----------|-------|---------|
| NFR-01 | Hiệu năng | Phản hồi chức năng chính < 3s (tải bình thường) | Cao |
| NFR-02 | Hiệu năng | Hỗ trợ tối thiểu 100 CCU | Cao |
| NFR-03 | Bảo mật | Mật khẩu hash; truyền tải HTTPS/TLS | Cao |
| NFR-04 | Phân quyền | RBAC: Customer, Host, Admin | Cao |
| NFR-05 | Toàn vẹn | Không double booking cùng thời gian | Cao |
| NFR-06 | Chịu lỗi | Lỗi thanh toán không mất dữ liệu booking | Cao |
| NFR-07 | Backup | Sao lưu định kỳ | Cao |
| NFR-08 | Mở rộng | Kiến trúc scale được | Trung bình |
| NFR-09 | UI/UX | Responsive Web/Mobile | Cao |
| NFR-10 | Bảo trì | Modular architecture | Trung bình |
| NFR-11 | Uptime | ≥ 99% | Cao |
| NFR-12 | Usability | Ít bước thao tác; thông báo lỗi rõ ràng | Trung bình |

---

## 2. Yêu cầu chức năng (FR)

### 2.1 Quản lý tài khoản

| Mã | Yêu cầu | Mô tả | Ưu tiên |
|----|---------|-------|---------|
| FR-A-01 | Đăng ký | Email, mật khẩu, thông tin cơ bản; validate | Cao |
| FR-A-02 | Xác thực email | Link/OTP kích hoạt tài khoản | Cao |
| FR-A-03 | Đăng nhập | Email/password; phân quyền role | Cao |
| FR-A-04 | Quên mật khẩu | Reset qua email | Cao |
| FR-A-05 | Cập nhật thông tin | Họ tên, SĐT, avatar | Trung bình |
| FR-A-06 | Đăng xuất | Kết thúc session | Trung bình |

### 2.2 Đăng ký Host

| Mã | Yêu cầu | Mô tả | Ưu tiên |
|----|---------|-------|---------|
| FR-H-01 | Đăng ký Host | Gửi hồ sơ + giấy tờ | Cao |
| FR-H-02 | Kiểm duyệt | Admin duyệt hồ sơ | Cao |
| FR-H-03 | Cập nhật role | `role=host` sau duyệt | Cao |
| FR-H-04 | Profile Host | Host cập nhật thông tin kinh doanh | Trung bình |

### 2.3 Quản lý nơi cư trú

| Mã | Yêu cầu | Mô tả | Ưu tiên |
|----|---------|-------|---------|
| FR-R-01 | Đăng phòng | Host tạo CSLT/phòng; admin duyệt | Cao |
| FR-R-02 | Cập nhật phòng | Sửa thông tin | Cao |
| FR-R-03 | Dynamic pricing | Giá theo thời điểm | Trung bình |
| FR-R-04 | Trạng thái | active / paused / pending / draft | Cao |
| FR-R-05 | Hình ảnh | Upload ảnh minh họa | Trung bình |
| FR-R-06 | Đồng bộ lịch | Block lịch khi booking thành công | Cao |

### 2.4 Đặt phòng

| Mã | Yêu cầu | Mô tả | Ưu tiên |
|----|---------|-------|---------|
| FR-B-01 | Tìm kiếm | Lọc địa điểm, giá, tiện ích, số khách | Cao |
| FR-B-02 | Chi tiết | Full thông tin trước khi đặt | Cao |
| FR-B-03 | Giữ phòng | Lock tạm khi chờ thanh toán | Cao |
| FR-B-04 | Tạo booking | Lưu record sau quy trình | Cao |
| FR-B-05 | Hủy booking | Hủy theo chính sách | Trung bình |
| FR-B-06 | Thông báo | Email/notification cho host và khách | Trung bình |

### 2.5 Thanh toán

| Mã | Yêu cầu | Mô tả | Ưu tiên |
|----|---------|-------|---------|
| FR-P-01 | Online | Chuyển khoản qua gateway | Cao |
| FR-P-02 | Tiền mặt | Trả khi check-in | Trung bình |
| FR-P-03 | Verify | Xác minh callback gateway | Cao |
| FR-P-04 | Trạng thái | Đã thanh toán / thất bại | Cao |
| FR-P-05 | Lịch sử | Log đối soát | Trung bình |

### 2.6 Quản lý lưu trú

| Mã | Yêu cầu | Mô tả | Ưu tiên |
|----|---------|-------|---------|
| FR-S-01 | Check-in | Nhận phòng | Cao |
| FR-S-02 | Check-out | Trả phòng | Cao |
| FR-S-03 | Tranh chấp | Mở ticket hỗ trợ | Trung bình |
| FR-S-04 | Review | Đánh giá sau lưu trú | Trung bình |
| FR-S-05 | Trạng thái lưu trú | Cập nhật lifecycle booking | Cao |

### 2.7 Yêu cầu mở rộng (đã triển khai ngoài SRS gốc)

| Mã | Yêu cầu | Mô tả |
|----|---------|-------|
| FR-X-01 | Smart Match | Tìm phòng bằng ngôn ngữ tự nhiên (TF-IDF) |
| FR-X-02 | AI Chat | Trợ lý Groq cho customer và host |
| FR-X-03 | Trợ lý vận hành thông minh | Chân dung khách, radar bảo trì, gợi ý giá & doanh thu (ML — hiện giả lập) |
| FR-X-04 | Tin nhắn | Chat hai chiều guest ↔ host |
| FR-X-05 | Ví xu & hạng thành viên | Loyalty customer |
| FR-X-06 | Yêu thích | Lưu CSLT yêu thích |

---

## 3. Quy trình nghiệp vụ (theo triển khai hiện tại)

### 3.1 Đăng ký & đăng nhập

**Luồng thực tế:**
- `POST /register` → tạo `User` role `guest`, token verify → redirect `verify_notice.html`.
- `GET /verify-email/<token>` → `is_email_verified=True`.
- `POST /login` → Flask-Login session; redirect `/customer/`, `/host/`, `/admin/` theo role.
- `GET /logout` → kết thúc session.

**Quy tắc:**
- Email unique (`users.email`).
- Mật khẩu Werkzeug hash.
- Login sai nhiều lần: cột `failed_login_attempts`, `is_locked` (admin có thể toggle lock).
- Quên MK: logic token trong `auth/routes.py` — template `forgot_password.html` / `reset_password.html` **chưa có** → route 404.

### 3.2 Host onboarding

**Luồng thực tế:**
- `GET/POST /customer/become-host` — lưu `id_card`, `host_document_path`, `host_status=pending`.
- Template `host_registration.html` **thiếu** → 404; trang marketing `become-host.html` chỉ tĩnh.
- Admin `POST /admin/hosts/<id>/approve` → `role=host`, `host_status=approved`.
- Admin reject → `host_status=rejected`.

### 3.3 Đặt phòng

**Luồng thực tế:**

```text
Tìm kiếm (/customer/search) hoặc Smart Match (/customer/smart-search)
  → Chi tiết CSLT (/customer/accommodation/<id>)
  → POST /customer/booking/create/<room_id>
  → Booking status=holding, hold_expiry_at = now + 20 phút
  → Checkout (/customer/booking/checkout/<code>)
  → Thanh toán → order detail
```

**Quy tắc:**
- Overlap check với booking `confirmed` + `holding` tại thời điểm POST create.
- Homestay/Villa (`books_whole_unit`): chặn mọi phòng trong CSLT.
- Khách vãng lai: `guest_id=NULL`, session `anonymous_booking_codes`.
- Hết 20 phút: hủy lazy khi truy cập checkout/payment — không có cron.
- Ô ngày trên search bar **chưa** lọc availability backend.
- Customer **chưa có** route hủy booking.

### 3.4 Thanh toán

**Luồng thực tế:**
- Checkout chọn **Thanh toán tiền mặt** → `status=confirmed`, `payment_status=pending`, `commission_fee` 15%.
- Checkout chọn **Thanh toán online** → `/customer/booking/payment/online/<code>`:
  - QR VietinBank mock, countdown `hold_expiry_at`.
  - Nút "Tôi đã chuyển khoản" → popup ~3s → `POST confirm` → callback `?status=success` → `payment_status=paid`.
- Mã promo checkout: `WELCOME10` (10%), `ROVVA50` (50.000đ) — hardcoded.
- Checkbox xu: giảm 50.000đ — **chưa** ghi `wallet_transactions`.
- Gateway thật: **không** — mock hoàn toàn.

### 3.5 Quản lý CSLT (Host)

**Luồng thực tế:**
- Host CRUD tại `/host/accommodation/accommodations/`.
- CSLT mới thường `status=pending` — admin duyệt tại portal.
- Phòng: create/edit/pause/delete; `base_price` integer VND/đêm.
- Trang pricing (`room/pricing.html`) — UI demo, **chưa** lưu giá theo ngày.
- Ảnh: file tĩnh theo ID + script fill; host profile có upload avatar.

### 3.6 Lưu trú, review, tranh chấp

- Booking `completed`: admin đặt thủ công qua portal — **không** auto sau ngày check-out.
- Review: member viết tại `/customer/account/reviews/write/<booking_id>` khi booking `completed`.
- Dispute: host phản hồi + admin resolve; customer **không** mở ticket.
- Check-in/check-out: **chưa** có route.

---

## 4. Phụ lục — Ánh xạ triển khai

### 4.1 Công nghệ

| Thành phần | Triển khai |
|------------|------------|
| Backend | Flask 3, Python 3.10+ |
| ORM / DB | SQLAlchemy, SQLite 13 bảng |
| Auth | Flask-Login, Werkzeug hash |
| Frontend | Jinja2, Bootstrap 5.3.8, Vanilla JS |
| AI | scikit-learn (Smart Match), Groq (chat) |

### 4.2 Hằng số nghiệp vụ

| Hằng số | Giá trị | File |
|---------|---------|------|
| Giữ chỗ | 20 phút | `booking.py` — `HOLD_MINUTES = 20` |
| Hoa hồng | 15% | `booking.py` — checkout |
| Host share | 90% | `host/payment.py` — `HOST_SHARE = 0.9` |
| Giảm xu | 50.000đ | `booking.py` — `XU_DISCOUNT` |
| Promo codes | WELCOME10, ROVVA50 | `booking.py` — `PROMO_CODES` |

### 4.3 Routes chính

Xem [ARCHITECTURE.md](ARCHITECTURE.md) và [ManHinh.md](ManHinh.md).

### 4.4 Tài khoản demo

| Role | Email | Password |
|------|-------|----------|
| Customer | `1@ss` | `1` |
| Host | `van.quangia@rova.vn` | `password123` |
| Admin | `admin@rova.vn` | `admin123` |

---

## 5. Tài liệu liên quan

- [BAO_CAO_SRS.md](BAO_CAO_SRS.md) — Bảng đối chiếu FR/NFR ↔ trạng thái code
- [ERD.md](ERD.md) — Schema database
- [ARCHITECTURE.md](ARCHITECTURE.md) — Kiến trúc kỹ thuật
- [ManHinh.md](ManHinh.md) — Mô tả màn hình

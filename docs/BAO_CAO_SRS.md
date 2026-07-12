# Báo cáo tiến độ — đối chiếu SRS

> Đối chiếu `docs/SRS.md` với codebase ROVVA tại **12/07/2026**.  
> Chỉ mô tả những gì **có hoặc chưa có** trong mã nguồn — không thêm tính năng giả định.

---

## Tóm tắt

| Hạng mục | Trạng thái |
|----------|------------|
| Luồng Customer (tìm → đặt → thanh toán → đơn) | ✅ End-to-end |
| Thanh toán online QR + tiền mặt (mock) | ✅ |
| Smart Match (TF-IDF + cosine) | ✅ |
| Tin nhắn khách ↔ host | ✅ |
| Customer SSR + dữ liệu DB | ✅ |
| Ảnh demo CSLT (~104 JPG, 12 CSLT) | ✅ |
| Admin portal SPA (9 view) | ✅ |
| Host (CSLT, booking, payment, dispute, message, promotion, report) | ✅ |
| AI Chat Groq (customer + host) | ✅ (cần API key) |
| Trợ lý vận hành thông minh | ✅ Dashboard; trang module riêng ⚠️ chưa route |
| Ví xu + promotion host tại checkout | 🟡 UI có; logic chưa khép |
| Auth forgot/reset password | ⚠️ Logic có; template thiếu → 404 |
| Become-host form | ⚠️ Route có; template thiếu → 404 |
| Email SMTP / payment gateway thật | 🔴 Mock |
| Hủy booking / check-in-out customer | 🔴 Chưa route |
| Automated tests | 🔴 Chưa có thư mục `tests/` |

**Ước lượng:** ~**72–78%** FR cốt lõi; đủ demo đồ án + báo cáo.

---

## Killer features (ngoài SRS gốc)

| Feature | Mô tả | Trạng thái |
|---------|-------|------------|
| Smart Match | Câu tiếng Việt → gợi ý phòng từ DB | ✅ |
| AI Chat (Groq) | Bubble + full page customer/host | ✅ |
| Trợ lý vận hành thông minh | Chân dung khách, radar bảo trì, gợi ý giá & doanh thu | 🟡 Dashboard ✅; gợi ý doanh thu **giả lập** (chưa ML) |
| Media theo ID | Ảnh + placeholder SVG | ✅ |
| QR VietinBank | Countdown 20 phút + popup xác nhận | ✅ mock |
| Hạng thành viên | Tier từ chi tiêu `completed` 365 ngày | ✅ hiển thị; chưa giảm giá theo tier |
| Tin nhắn realtime UI | Conversation + Message | ✅ SSR refresh |

---

## 1. Yêu cầu chức năng (FR)

Chú thích: ✅ Hoàn thành · 🟡 Một phần · 🔴 Chưa · ⚠️ Route/template lỗi

### 2.1 Quản lý tài khoản

| ID | Yêu cầu | TT | Ghi chú |
|----|---------|-----|---------|
| FR-A-01 | Đăng ký | ✅ | `auth/register.html`; validate unique email |
| FR-A-02 | Xác thực email | 🟡 | Token + `/verify-email/<token>`; không gửi SMTP |
| FR-A-03 | Đăng nhập + phân quyền | 🟡 | Redirect role OK; host route chưa guard `role=host` |
| FR-A-04 | Quên mật khẩu | ⚠️ | Logic token trong `auth/routes.py`; `forgot_password.html`, `reset_password.html` thiếu |
| FR-A-05 | Cập nhật thông tin | ✅ | Customer profile; host profile + avatar upload |
| FR-A-06 | Đăng xuất | ✅ | `/logout` |
| — | Bảo mật | ✅ | `account/security` — đổi MK, xóa TK (modal 2 bước) |

### 2.2 Đăng ký Host

| ID | Yêu cầu | TT | Ghi chú |
|----|---------|-----|---------|
| FR-H-01 | Đăng ký Host | ⚠️ | `/customer/become-host` — `host_registration.html` thiếu |
| FR-H-02 | Kiểm duyệt | ✅ | Admin portal approve/reject |
| FR-H-03 | Cập nhật role | ✅ | Approve → `role=host` |
| FR-H-04 | Profile Host | ✅ | `/host/profile` |

### 2.3 Quản lý nơi cư trú

| ID | Yêu cầu | TT | Ghi chú |
|----|---------|-----|---------|
| FR-R-01 | Đăng phòng | ✅ | CRUD CSLT + room; admin duyệt |
| FR-R-02 | Cập nhật | ✅ | Form edit |
| FR-R-03 | Dynamic pricing | 🔴 | UI `pricing.html`; chỉ `base_price` |
| FR-R-04 | Trạng thái | ✅ | active/pending/paused/draft |
| FR-R-05 | Hình ảnh | 🟡 | Script fill + host avatar; upload CSLT một phần |
| FR-R-06 | Đồng bộ lịch | 🟡 | Overlap khi đặt; homestay/villa whole unit |

### 2.4 Đặt phòng

| ID | Yêu cầu | TT | Ghi chú |
|----|---------|-----|---------|
| FR-B-01 | Tìm kiếm | 🟡 | Filter SSR + Smart Match; ngày UI chưa lọc |
| FR-B-02 | Chi tiết | ✅ | `accommodation/detail.html` unified |
| FR-B-03 | Giữ phòng | ✅ | **20 phút** — `HOLD_MINUTES=20` |
| FR-B-04 | Tạo booking | ✅ | holding → checkout → confirmed |
| FR-B-05 | Hủy | 🔴 | Admin đổi status; customer không có route |
| FR-B-06 | Thông báo | 🔴 | Email mock log; host notification seed only |

### 2.5 Thanh toán

| ID | Yêu cầu | TT | Ghi chú |
|----|---------|-----|---------|
| FR-P-01 | Online | ✅ mock | QR + callback success |
| FR-P-02 | Tiền mặt | ✅ | `payment_status=pending` |
| FR-P-03 | Verify | 🟡 | User xác nhận; không verify ngân hàng |
| FR-P-04 | Trạng thái | 🟡 | Customer `paid` vs host `disbursed` — từ điển khác |
| FR-P-05 | Lịch sử | 🟡 | Wallet UI, host payment, admin; xu chưa trừ |

### 2.6 Quản lý lưu trú

| ID | Yêu cầu | TT | Ghi chú |
|----|---------|-----|---------|
| FR-S-01 | Check-in | 🔴 | — |
| FR-S-02 | Check-out | 🔴 | — |
| FR-S-03 | Tranh chấp | 🟡 | Host + admin; customer không mở ticket |
| FR-S-04 | Review | 🟡 | Route viết; cần admin set `completed` |
| FR-S-05 | Trạng thái lưu trú | 🔴 | Không auto `completed` |

### 2.7 Mở rộng (FR-X)

| ID | Yêu cầu | TT | Ghi chú |
|----|---------|-----|---------|
| FR-X-01 | Smart Match | ✅ | `smart_match.py` |
| FR-X-02 | AI Chat | ✅ | Cần `GROQ_API_KEY` |
| FR-X-03 | Trợ lý vận hành thông minh | 🟡 | Dashboard ✅; gợi ý giá/doanh thu giả lập, chưa ML |
| FR-X-04 | Tin nhắn | ✅ | `customer_messages.py` |
| FR-X-05 | Ví xu & tier | 🟡 | Hiển thị ✅; checkout xu chưa trừ DB |
| FR-X-06 | Yêu thích | ✅ | Toggle API + favorites page |

---

## 2. Yêu cầu phi chức năng (NFR)

| ID | Hạng mục | TT | Ghi chú |
|----|----------|-----|---------|
| NFR-01 | < 3s | ✅ dev | SQLite, dataset nhỏ |
| NFR-02 | 100 CCU | 🔴 | Chưa load test |
| NFR-03 | Bảo mật | 🟡 | Hash ✅; HTTPS chưa |
| NFR-04 | RBAC | 🟡 | Admin guard; host chưa siết role |
| NFR-05 | No double book | 🟡 | Overlap query; chưa DB lock |
| NFR-06 | Chịu lỗi TT | 🟡 | Mock cơ bản |
| NFR-07 | Backup | 🔴 | — |
| NFR-08 | Mở rộng | ✅ | Blueprint + services |
| NFR-09 | Responsive | ✅ | Bootstrap 5 |
| NFR-10 | Modular | ✅ | Factory pattern |
| NFR-11 | Uptime 99% | 🔴 | Dev only |
| NFR-12 | Usability | 🟡 | Flash messages; template legacy còn |

---

## 3. Đã hoàn thành (checklist code)

### Nền tảng
- [x] Flask application factory (`backend/app/__init__.py`)
- [x] 13 bảng SQLite — [ERD.md](ERD.md)
- [x] Seed + patch schema startup (`seed.py`)
- [x] Role redirect `/` → customer/host/admin

### Customer (71 templates)
- [x] Home guest/member, search, smart-search
- [x] Chi tiết CSLT, checkout, payment online, order detail
- [x] Trips, profile, wallet, tier, favorites, reviews, messages, security
- [x] AI chat `/customer/chat`, blog, marketing/support catch-all

### Host (43 templates)
- [x] Dashboard, notifications, profile, AI chat
- [x] CRUD CSLT/phòng, booking, payment, dispute, message
- [x] Promotion, report, support docs (11 trang)
- [x] Trợ lý vận hành thông minh — persona, maintenance, gợi ý doanh thu (giả lập)

### Admin (24 templates)
- [x] Portal SPA `portal.html` + 9 view partials
- [x] Legacy pages không dùng — redirect về portal

### Services
- [x] `smart_match.py`, `ai_chat.py`, `host_copilot/*`
- [x] `customer_messages.py`, `member_tier.py`, `admin_portal.py`

### Media
- [x] `scripts/fill_accommodation_images.py`
- [x] Placeholder SVG (`utils/media.py`)

---

## 4. Chưa hoàn thành / thiếu

### Ưu tiên cao (ảnh hưởng demo)
1. Template `host_registration.html`, `forgot_password.html`, `reset_password.html`
2. Kết nối route trang trợ lý vận hành thông minh
3. Route hủy booking customer
4. Thống nhất `payment_status`
5. Hook notification runtime
6. Trừ xu + promotion host tại checkout

### Ngoài phạm vi đồ án
7. SMTP, payment gateway thật
8. Dynamic pricing theo ngày
9. Check-in/out tự động
10. pytest / load test / production deploy

---

## 5. Thống kê

| Metric | Giá trị |
|--------|---------|
| Models (bảng) | 13 |
| Blueprints registered | 13 (chưa gồm trang trợ lý vận hành) |
| HTML templates | 144 |
| Giữ chỗ | 20 phút |
| CSLT seed | 12 |
| Phòng seed | 32 |
| Booking seed | 14 |
| FR hoàn thành (ước lượng) | ~28/36 (~78%) |
| NFR hoàn thành (ước lượng) | ~5/12 (~42%) |

---

## 6. Tài khoản demo

| Vai trò | Email | Mật khẩu |
|---------|-------|----------|
| Customer | `1@ss` | `1` |
| Host | `van.quangia@rova.vn` | `password123` |
| Admin | `admin@rova.vn` | `admin123` |
| Host pending | `host.pending@rova.vn` | `123456` |

---

## 7. Tài liệu liên quan

- [SRS.md](SRS.md)
- [ERD.md](ERD.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [ManHinh.md](ManHinh.md)
- [README.md](../README.md)

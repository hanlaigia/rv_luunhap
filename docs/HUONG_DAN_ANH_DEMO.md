# Hướng dẫn ảnh demo — ROVVA

> **Cập nhật:** 12/07/2026 — bám sát `utils/media.py`, models và `scripts/fill_accommodation_images.py`.

Ảnh cơ sở lưu trú, phòng và avatar **không lưu BLOB trong database**. Hệ thống dùng file tĩnh theo quy ước ID, với fallback SVG khi thiếu file.

---

## Quy ước đường dẫn

| Loại | Đường dẫn tĩnh | Property / helper |
|------|----------------|-------------------|
| Ảnh bìa CSLT | `frontend/static/customer/images/accommodations/<acc_id>/cover.jpg` | `Accommodation.cover_url` |
| Gallery CSLT | `.../accommodations/<acc_id>/gallery/*.jpg` | Dùng trong detail template |
| Ảnh phòng | `.../accommodations/<acc_id>/rooms/<room_id>.jpg` | `Room.image_url` |
| Avatar user | `frontend/static/customer/images/avatars/<user_id>.jpg` | `User.avatar_url` |
| QR thanh toán | `frontend/static/customer/images/payment/qr-vietinbank.png` | Template `payment/online.html` |
| Placeholder | `frontend/static/customer/images/placeholders/*.svg` | `utils/media.resolve_media()` |

**Placeholders có sẵn:**
- `accommodation.svg` — thiếu cover CSLT
- `room.svg` — thiếu ảnh phòng
- `avatar.svg` — thiếu avatar

---

## Logic fallback (`utils/media.py`)

1. Kiểm tra file vật lý tồn tại trong `frontend/static/`.
2. Nếu không có → trả URL placeholder SVG tương ứng.
3. Template dùng `cover_url`, `image_url`, `avatar_url` — **không** hardcode path DB cột `image`/`avatar` legacy.

---

## Script điền ảnh demo

Chạy từ thư mục gốc dự án:

```powershell
py scripts/fill_accommodation_images.py
```

Script (`scripts/fill_accommodation_images.py`) thực hiện:

1. **Đổi tên file phòng** theo `room_id` thật trong DB.
2. **Copy ảnh donor** từ CSLT đã có sang CSLT thiếu — map theo loại hình (`TYPE_DONOR`: Homestay→1, Villa→2, Khách sạn→3, Resort→6, …).
3. **Tải ảnh Unsplash** cho một số CSLT hotel/resort/căn hộ (`EXTRA_COVERS` — acc_id 4, 5, 9, 10, 11, 12).

**Yêu cầu:** DB đã seed (`py -m flask --app run seed`) để script đọc đúng `room_id` / `acc_id`.

---

## Dữ liệu seed liên quan

| Metric | Giá trị |
|--------|---------|
| CSLT | 12 |
| Phòng | 32 (28 active) |
| Ảnh JPG demo | ~104 |
| Avatar demo | `avatars/1.jpg` … `4.jpg` |

Seed tạo CSLT tại: Đà Lạt, Hội An, Nha Trang, Đà Nẵng, Vũng Tàu, … — phục vụ Smart Match và demo UI.

---

## Upload qua UI (trạng thái code)

| Khu vực | Trạng thái |
|---------|------------|
| Host profile | ✅ Upload avatar — `POST /host/profile/edit` |
| Form CSLT / phòng | 🟡 UI chọn ảnh; demo chủ yếu dùng script + path theo ID |
| Customer profile | 🟡 Hiển thị `avatar_url`; chưa có route upload customer |

---

## Ảnh tham chiếu trong template nhưng có thể thiếu file

Một số template tham chiếu path chưa có trên disk (UI vẫn fallback hoặc broken image tùy trường hợp):

- `customer/images/logos/Logo.jpg`
- `customer/images/banners/*`
- `shared/images/footer-resort.png`, `footer-logo.png`

Không ảnh hưởng luồng đặt phòng chính — CSLT demo dùng `accommodations/<id>/`.

---

## Quy trình setup ảnh cho môi trường mới

```powershell
py -m flask --app run seed
py scripts/fill_accommodation_images.py
py run.py
```

Kiểm tra: mở `/customer/accommodation/1` — gallery và cover hiển thị; nếu xóa file → placeholder SVG.

---

## Tài liệu liên quan

- [ERD.md](ERD.md) — ghi chú media
- [ARCHITECTURE.md](ARCHITECTURE.md) — mục Media & static files
- [README.md](../README.md)

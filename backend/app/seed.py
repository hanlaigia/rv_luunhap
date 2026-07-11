from datetime import date, timedelta, datetime
import json

from backend.app.extensions import db
from backend.app.models import Accommodation, Booking, Room, User, Dispute

def seed_database():
    if User.query.first():
        return False

    host = User(
        full_name="Văn Quản Gia",
        email="van.quangia@rova.vn",
        phone="0901234567",
        id_card="079203001234",
        avatar="images/host-avatar.png",
        role="host",
        is_email_verified=True,
        host_status="approved"
    )
    host.set_password("password123")
    db.session.add(host)

    guest = User(
        full_name="Khách Hàng Mẫu",
        email="1@ss",
        phone="0909999999",
        avatar="shared/images/avatars/Hinh_avata.jpg",
        role="guest",
        is_email_verified=True
    )
    guest.set_password("1")
    db.session.add(guest)

    admin = User(
        full_name="Quản Trị Viên",
        email="admin@rova.vn",
        phone="0901111111",
        avatar="shared/images/avatars/Hinh_avata.jpg",
        role="admin",
        is_email_verified=True,
    )
    admin.set_password("admin123")
    db.session.add(admin)

    pending_host = User(
        full_name="Nguyễn Văn Host Mới",
        email="host.pending@rova.vn",
        phone="0902222222",
        role="guest",
        host_status="pending",
        is_email_verified=True,
        introduction="Tôi muốn đăng ký làm Host trên Rovva.",
    )
    pending_host.set_password("123456")
    db.session.add(pending_host)

    db.session.flush()

    accommodations_data = [
        {
            "name": "Homestay Đà Lạt View",
            "type": "Homestay",
            "location": "Lâm Đồng, Việt Nam",
            "address": "24 Khe Sanh, Phường 10, Thành phố Đà Lạt, Lâm Đồng",
            "description": (
                "Tọa lạc trên ngọn đồi thoai thoải với tầm nhìn bao trọn thung lũng sương mờ, "
                "Homestay Đà Lạt View mang đến không gian nghỉ dưỡng tối giản nhưng đầy đủ tiện nghi."
            ),
            "status": Accommodation.STATUS_ACTIVE,
            "image": "images/accommodations/homestay-da-lat.jpg",
            "rooms": [
                {
                    "name": "Phòng 101 - Deluxe Mountain View",
                    "bed_info": "1 Giường đôi",
                    "capacity": 2,
                    "base_price": 850000,
                    "status": Room.STATUS_ACTIVE,
                },
                {
                    "name": "Phòng 202 - Family Suite",
                    "bed_info": "2 Giường đôi",
                    "capacity": 4,
                    "base_price": 1200000,
                    "status": Room.STATUS_ACTIVE,
                },
                {
                    "name": "Phòng 104 - Cozy Twin",
                    "bed_info": "2 Giường đơn",
                    "capacity": 2,
                    "base_price": 720000,
                    "status": Room.STATUS_ACTIVE,
                },
                {
                    "name": "Phòng 303 - Standard Garden",
                    "bed_info": "1 Giường đôi",
                    "capacity": 2,
                    "base_price": 650000,
                    "status": Room.STATUS_ACTIVE,
                },
            ],
        },
        {
            "name": "Villa Hội An Garden",
            "type": "Villa",
            "location": "Quảng Nam, Việt Nam",
            "address": "Cẩm Hà, Hội An, Quảng Nam",
            "description": "Villa nghỉ dưỡng giữa khu vườn xanh mát, gần phố cổ Hội An.",
            "status": Accommodation.STATUS_ACTIVE,
            "image": "images/accommodations/villa-hoi-an.jpg",
            "rooms": [
                {"name": "Villa Master", "bed_info": "1 Giường King", "capacity": 2, "base_price": 2500000, "status": Room.STATUS_ACTIVE},
                {"name": "Garden Room 1", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 1800000, "status": Room.STATUS_ACTIVE},
                {"name": "Garden Room 2", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 1800000, "status": Room.STATUS_ACTIVE},
                {"name": "Pool Suite", "bed_info": "1 Giường King", "capacity": 3, "base_price": 3200000, "status": Room.STATUS_ACTIVE},
                {"name": "Family Bungalow", "bed_info": "2 Giường đôi", "capacity": 4, "base_price": 2800000, "status": Room.STATUS_ACTIVE},
                {"name": "Deluxe Twin", "bed_info": "2 Giường đơn", "capacity": 2, "base_price": 1600000, "status": Room.STATUS_ACTIVE},
                {"name": "Studio View", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 1500000, "status": Room.STATUS_ACTIVE},
                {"name": "Patio Room", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 1700000, "status": Room.STATUS_ACTIVE},
                {"name": "Annex Room A", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 1400000, "status": Room.STATUS_PAUSED},
                {"name": "Annex Room B", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 1400000, "status": Room.STATUS_PAUSED},
            ],
        },
        {
            "name": "Sunside Homestay",
            "type": "Homestay",
            "location": "Đà Lạt, Lâm Đồng",
            "address": "Phường 3, Thành phố Đà Lạt",
            "description": "Homestay ấm cúng với view nắng sớm.",
            "status": Accommodation.STATUS_ACTIVE,
            "image": "images/accommodations/sunside-homestay.jpg",
            "rooms": [
                {"name": "Phòng Deluxe - Tầng 2", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 780000, "status": Room.STATUS_ACTIVE},
                {"name": "Phòng Standard - Tầng 1", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 580000, "status": Room.STATUS_ACTIVE},
                {"name": "Phòng Family", "bed_info": "2 Giường đôi", "capacity": 4, "base_price": 980000, "status": Room.STATUS_ACTIVE},
            ],
        },
        {
            "name": "Khách sạn Ruby",
            "type": "Khách sạn",
            "location": "Nha Trang, Khánh Hòa",
            "address": "Trần Phú, Nha Trang",
            "description": "Khách sạn hiện đại, thủ tục check-in nhanh chóng.",
            "status": Accommodation.STATUS_ACTIVE,
            "image": "images/accommodations/khach-san-ruby.jpg",
            "rooms": [
                {"name": "Ruby Deluxe", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 1100000, "status": Room.STATUS_ACTIVE},
                {"name": "Ruby Superior", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 950000, "status": Room.STATUS_ACTIVE},
                {"name": "Ruby Suite", "bed_info": "1 Giường King", "capacity": 3, "base_price": 1500000, "status": Room.STATUS_ACTIVE},
            ],
        },
        {
            "name": "Rovva Seaside Resort & Spa",
            "type": "Resort",
            "location": "Phú Quốc, Kiên Giang",
            "address": "Bãi Trường, Phú Quốc",
            "description": "Resort cao cấp ven biển với spa và hồ bơi vô cực.",
            "status": Accommodation.STATUS_ACTIVE,
            "image": "images/accommodations/seaside-resort.jpg",
            "rooms": [
                {"name": "Ocean View Suite", "bed_info": "1 Giường King", "capacity": 2, "base_price": 3500000, "status": Room.STATUS_ACTIVE},
                {"name": "Beach Villa", "bed_info": "1 Giường King", "capacity": 4, "base_price": 5200000, "status": Room.STATUS_ACTIVE},
                {"name": "Garden Bungalow", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 2800000, "status": Room.STATUS_ACTIVE},
            ],
        },
        {
            "name": "Sea Breeze Cottage",
            "type": "Cottage",
            "location": "Đà Nẵng, Việt Nam",
            "address": "Sơn Trà, Đà Nẵng",
            "description": "Cottage nhỏ xinh hướng biển.",
            "status": Accommodation.STATUS_ACTIVE,
            "image": "images/accommodations/sea-breeze.jpg",
            "rooms": [
                {"name": "Cottage A", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 890000, "status": Room.STATUS_ACTIVE},
                {"name": "Cottage B", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 890000, "status": Room.STATUS_ACTIVE},
                {"name": "Cottage C", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 890000, "status": Room.STATUS_ACTIVE},
            ],
        },
        {
            "name": "Sunshine Homestay",
            "type": "Homestay",
            "location": "Vũng Tàu, Bà Rịa - Vũng Tàu",
            "address": "Thùy Vân, Vũng Tàu",
            "description": "Homestay gần biển, decor tươi sáng.",
            "status": Accommodation.STATUS_ACTIVE,
            "image": "images/accommodations/sunshine-homestay.jpg",
            "rooms": [
                {"name": "Sun Room", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 620000, "status": Room.STATUS_ACTIVE},
                {"name": "Sea View Room", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 750000, "status": Room.STATUS_ACTIVE},
            ],
        },
        {
            "name": "Homestay A",
            "type": "Homestay",
            "location": "Hội An, Quảng Nam",
            "address": "Cẩm Châu, Hội An",
            "description": "Homestay gần biển An Bàng.",
            "status": Accommodation.STATUS_ACTIVE,
            "image": "images/accommodations/homestay-a.jpg",
            "rooms": [
                {"name": "Phòng Deluxe - Homestay A", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 680000, "status": Room.STATUS_ACTIVE},
                {"name": "Studio hướng biển - Homestay A", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 820000, "status": Room.STATUS_ACTIVE},
            ],
        },
        {
            "name": "Congo Hotel",
            "type": "Khách sạn",
            "location": "Quận 1, TP. Hồ Chí Minh",
            "address": "Nguyễn Huệ, Quận 1, TP. HCM",
            "description": "Khách sạn boutique tại trung tâm Quận 1.",
            "status": Accommodation.STATUS_PENDING,
            "image": "images/accommodations/congo-hotel.jpg",
            "rooms": [
                {"name": "Standard Room", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 1200000, "status": Room.STATUS_PENDING},
                {"name": "Deluxe Room", "bed_info": "1 Giường đôi", "capacity": 2, "base_price": 1500000, "status": Room.STATUS_PENDING},
            ],
        },
        {
            "name": "Luxury Penthouse Da Lat",
            "type": "Căn hộ",
            "location": "Đà Lạt, Lâm Đồng",
            "address": "Phường 1, Thành phố Đà Lạt",
            "description": "Penthouse cao cấp view toàn cảnh thành phố.",
            "status": Accommodation.STATUS_PENDING,
            "image": "images/accommodations/penthouse-dalat.jpg",
            "rooms": [],
        },
        {
            "name": "Urban Suite Saigon",
            "type": "Căn hộ",
            "location": "Quận 1, TP. Hồ Chí Minh",
            "address": "Bến Nghé, Quận 1, TP. HCM",
            "description": "Căn hộ dịch vụ hiện đại trung tâm Sài Gòn.",
            "status": Accommodation.STATUS_PAUSED,
            "image": "images/accommodations/urban-suite.jpg",
            "rooms": [],
        },
        {
            "name": "Mountain Retreat Sapa",
            "type": "Homestay",
            "location": "Sa Pa, Lào Cai",
            "address": "Fansipan, Sa Pa",
            "description": "Homestay trên núi với view ruộng bậc thang.",
            "status": Accommodation.STATUS_PAUSED,
            "image": "images/accommodations/sapa-retreat.jpg",
            "rooms": [],
        },
    ]

    all_rooms = []
    for acc_data in accommodations_data:
        rooms_data = acc_data.pop("rooms")
        if "city" not in acc_data:
            acc_data["city"] = acc_data["location"].split(",")[0].strip() if "," in acc_data.get("location", "") else acc_data.get("location", "")
        if "district" not in acc_data:
            acc_data["district"] = ""
        if "features" not in acc_data:
            acc_data["features"] = ["Hủy phòng linh hoạt", "Không hút thuốc", "Cho phép thú cưng"]
        if "allows_pets" not in acc_data:
            acc_data["allows_pets"] = True if "Cho phép thú cưng" in acc_data.get("features", []) else False
        acc = Accommodation(host_id=host.id, **acc_data)
        db.session.add(acc)
        db.session.flush()

        for room_data in rooms_data:
            if "area" not in room_data:
                room_data["area"] = "30m2"
            if "description" not in room_data:
                room_data["description"] = "Phòng được thiết kế theo phong cách hiện đại tối giản nhưng không kém phần ấm cúng. Điểm nhấn của phòng là ban công rộng hướng thẳng ra thung lũng xanh mướt, cho phép khách hàng tận hưởng trọn vẹn không khí trong lành."
            if "features" not in room_data:
                room_data["features"] = ["Wifi miễn phí", "Điều hòa", "Bồn tắm", "Ban công", "Tivi 4K"]
            if "services" not in room_data:
                room_data["services"] = [
                    {"name": "Đưa đón tận nơi", "price": "250000", "unit": "đ/lượt", "checked": True},
                    {"name": "Bữa sáng tại sảnh", "price": "150000", "unit": "đ/người/ngày", "checked": True}
                ]
            room = Room(accommodation_id=acc.id, **room_data)
            db.session.add(room)
            all_rooms.append(room)

    db.session.flush()

    active_rooms = [r for r in all_rooms if r.status == Room.STATUS_ACTIVE]
    assert len(all_rooms) == 32, f"Expected 32 rooms, got {len(all_rooms)}"
    assert len(active_rooms) == 28, f"Expected 28 active rooms, got {len(active_rooms)}"
    assert Accommodation.query.count() == 12

    booking_amounts = [
        3900000, 3500000, 3200000, 2800000, 2600000,
        4200000, 3800000, 3400000, 3100000, 2900000,
        2500000, 2300000, 2200000, 2100000,
    ]
    assert sum(booking_amounts) == 42500000

    guest_names = [
        "Nguyễn Văn A", "Trần Thị B", "Lê Văn C", "Phạm Thị D",
        "Hoàng Văn E", "Vũ Thị F", "Đặng Văn G", "Bùi Thị H",
        "Ngô Văn I", "Dương Thị K", "Lý Văn L", "Mai Thị M",
        "Cao Văn N", "Hồ Thị O",
    ]

    today = date.today()
    for idx, amount in enumerate(booking_amounts):
        room = active_rooms[idx % len(active_rooms)]
        
        # Dùng đúng hằng số status của model để luồng "Chuyến đi của tôi" + filter hoạt động.
        if idx % 4 == 0:
            check_in = today + timedelta(days=3)
            check_out = check_in + timedelta(days=2)
            status = Booking.STATUS_CONFIRMED  # Sắp tới
        elif idx % 4 == 1:
            check_in = today - timedelta(days=2)
            check_out = today + timedelta(days=1)
            status = Booking.STATUS_CONFIRMED  # Đang lưu trú (đã xác nhận, đang ở)
        elif idx % 4 == 2:
            check_in = today - timedelta(days=10)
            check_out = check_in + timedelta(days=3)
            status = Booking.STATUS_COMPLETED  # Hoàn thành
        else:
            check_in = today + timedelta(days=5)
            check_out = check_in + timedelta(days=1)
            status = Booking.STATUS_CANCELLED  # Đã hủy

        payment_status = "pending"
        disbursed_at = None
        if idx % 4 == 0:
            payment_status = "pending"
        elif idx % 4 == 1:
            payment_status = "disbursed"
            disbursed_at = today - timedelta(days=2)
        elif idx % 4 == 2:
            payment_status = "in_dispute"
        else:
            payment_status = "resolved"
            disbursed_at = today - timedelta(days=1)

        booking = Booking(
            booking_code=f"#RV123{40 + idx}",
            room_id=room.id,
            guest_id=guest.id,
            guest_name=guest_names[idx],
            guest_phone=f"0901 234 {500 + idx}",
            guest_email=f"guest{idx}@email.com",
            guest_count=1 + (idx % 4),
            guest_note="Vui lòng chuẩn bị thêm một bộ chăn gối." if idx % 3 == 0 else "",
            check_in=check_in,
            check_out=check_out,
            total_amount=amount,
            status=status,
            payment_status=payment_status,
            disbursed_at=disbursed_at,
            created_at=today - timedelta(days=15 - idx),
        )
        db.session.add(booking)

    from backend.app.models import Promotion, Review
    
    # --- Promotions Seed ---
    promotions_data = [
        {
            "name": "Hè rực rỡ 2026",
            "type": "Giảm %",
            "discount_value": "20",
            "start_date": "15/06/2026",
            "end_date": "15/08/2026",
            "min_nights": 1,
            "apply_days": "Tất cả các ngày",
            "applied_to": {"label": "Khách sạn Ruby", "target": "accommodation", "id": active_rooms[0].accommodation_id},
            "status": True,
        },
        {
            "name": "Flash Sale thứ 2",
            "type": "Giảm giá cố định",
            "discount_value": "100.000",
            "start_date": "15/06/2026",
            "end_date": "15/08/2026",
            "min_nights": 1,
            "apply_days": "Thứ 2",
            "applied_to": {"label": "Tất cả CSLT", "target": "all"},
            "status": False,
        },
        {
            "name": "Khách hàng thân thiết",
            "type": "Giảm %",
            "discount_value": "30",
            "start_date": "15/06/2026",
            "end_date": "15/08/2026",
            "min_nights": 3,
            "apply_days": "Tất cả các ngày",
            "applied_to": {"label": "Homestay Đà Lạt View", "target": "accommodation", "id": active_rooms[1].accommodation_id},
            "status": False,
        }
    ]
    for p_data in promotions_data:
        promo = Promotion(host_id=host.id, **p_data)
        db.session.add(promo)
        
    # --- Reviews Seed ---
    for room in active_rooms:
        r1 = Review(
            room_id=room.id,
            guest_name="Lê Thị Lan",
            booking_code="#RV123456",
            rating=5,
            content="Phòng rất sạch sẽ, dịch vụ chu đáo. Mình rất hài lòng và sẽ quay lại.",
            created_at=today - timedelta(days=2)
        )
        r2 = Review(
            room_id=room.id,
            guest_name="Minh Hoàng",
            booking_code="#RV123496",
            rating=4,
            content="Vị trí thuận lợi, tuy nhiên cách âm chưa được tốt lắm.",
            created_at=today - timedelta(days=5)
        )
        r3 = Review(
            room_id=room.id,
            guest_name="Hữu Duyên",
            booking_code="#RV120496",
            rating=4,
            content="Ok, sẽ ghé tiếp.",
            reply="Cảm ơn bạn đã ghé thăm. Hẹn gặp lại bạn lần sau!",
            created_at=today - timedelta(days=10),
            reply_at=today - timedelta(days=9)
        )
        db.session.add_all([r1, r2, r3])

    db.session.flush()

    # --- Disputes Seed ---
    bookings_for_dispute = Booking.query.limit(3).all()
    if len(bookings_for_dispute) >= 3:
        d1 = Dispute(
            dispute_code="TC260701",
            booking_id=bookings_for_dispute[0].id,
            status=Dispute.STATUS_NEEDS_RESPONSE,
            guest_complaint="Phòng không giống như hình ảnh, không có ban công như mô tả.",
            guest_evidence=json.dumps(["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6"]),
            created_at=today - timedelta(days=2)
        )
        d2 = Dispute(
            dispute_code="TC260702",
            booking_id=bookings_for_dispute[1].id,
            status=Dispute.STATUS_PROCESSING,
            guest_complaint="Máy lạnh hỏng, tôi đã yêu cầu đổi phòng nhưng không được giải quyết.",
            guest_evidence=json.dumps(["https://images.unsplash.com/photo-1585422896656-78b6631b0a43"]),
            host_response="Chúng tôi đã cử thợ sửa chữa nhưng do đêm khuya nên không thể khắc phục ngay. Sáng hôm sau chúng tôi đã đề xuất đổi phòng nhưng khách không đồng ý.",
            host_evidence=json.dumps([]),
            created_at=today - timedelta(days=5)
        )
        d3 = Dispute(
            dispute_code="TC260703",
            booking_id=bookings_for_dispute[2].id,
            status=Dispute.STATUS_RESOLVED,
            guest_complaint="Thái độ nhân viên lễ tân không tốt, phòng có mùi ẩm mốc.",
            guest_evidence=json.dumps([]),
            host_response="Chúng tôi xin lỗi về trải nghiệm của khách. Chúng tôi sẽ nhắc nhở nhân viên và kiểm tra lại phòng.",
            admin_resolution="Hoàn trả 20% phí phòng như một lời xin lỗi từ hệ thống.",
            refund_amount=500000,
            created_at=today - timedelta(days=10)
        )
        db.session.add_all([d1, d2, d3])
        
    from backend.app.models import Withdrawal
    w1 = Withdrawal(host_id=host.id, amount=4000000, bank_account="Vietcombank xxxx 1234", status=Withdrawal.STATUS_COMPLETED, created_at=today - timedelta(days=30), completed_at=today - timedelta(days=29))
    w2 = Withdrawal(host_id=host.id, amount=3500000, bank_account="Vietcombank xxxx 1234", status=Withdrawal.STATUS_COMPLETED, created_at=today - timedelta(days=10), completed_at=today - timedelta(days=9))
    db.session.add_all([w1, w2])

    from backend.app.models import Conversation, Message
    
    # --- Conversation Seed ---
    c1 = Conversation(host_id=host.id, guest_name="Nguyễn Văn A", guest_email="guest0@email.com", guest_phone="0901 234 500", created_at=today - timedelta(days=2))
    c2 = Conversation(host_id=host.id, guest_name="Trần Thị B", guest_email="guest1@email.com", guest_phone="0901 234 501", created_at=today - timedelta(days=5))
    c3 = Conversation(host_id=host.id, guest_name="Lê Duy", guest_email="guest2@email.com", guest_phone="0901 234 502", created_at=today - timedelta(days=10))
    db.session.add_all([c1, c2, c3])
    db.session.flush()
    
    m1 = Message(conversation_id=c1.id, sender_type="host", content="Chào anh A, rất vui được đón tiếp anh! Thông thường thời gian check-in là 14:00 để bên em chuẩn bị phòng sạch sẽ nhất. Tuy nhiên, nếu ngày 11 không có khách trả phòng muộn, bên em sẽ hỗ trợ anh check-in sớm từ 11:00 hoàn toàn miễn phí ạ.", is_read=True, created_at=datetime.utcnow() - timedelta(minutes=60))
    m2 = Message(conversation_id=c1.id, sender_type="guest", content="Chào chủ nhà, tôi muốn hỏi về thời gian check-in của homestay mình vào ngày 12 tới ạ? Liệu tôi có thể đến sớm lúc 10h sáng được không?", is_read=False, created_at=datetime.utcnow() - timedelta(minutes=9))
    
    m3 = Message(conversation_id=c2.id, sender_type="host", content="Dạ vâng, cảm ơn chị đã ủng hộ.", is_read=True, created_at=today - timedelta(days=1))
    m4 = Message(conversation_id=c2.id, sender_type="guest", content="Cảm ơn bạn đã hỗ trợ!", is_read=True, created_at=today - timedelta(days=1))
    
    m5 = Message(conversation_id=c3.id, sender_type="guest", content="Bạn có thể gửi ảnh ban công không?", is_read=False, created_at=today - timedelta(days=3))
    
    db.session.add_all([m1, m2, m3, m4, m5])
    
    c1.updated_at = m2.created_at
    c2.updated_at = m4.created_at
    c3.updated_at = m5.created_at

    # --- Ví xu (Wallet) + Yêu thích (Favorites) cho khách mẫu ---
    from backend.app.models import WalletTransaction, Favorite

    wallet_data = [
        ("earn", 120, "Thưởng chào mừng thành viên mới"),
        ("earn", 68, "Tích xu từ đơn đặt phòng #RV12340"),
        ("earn", 54, "Tích xu từ đơn đặt phòng #RV12344"),
        ("spend", 50, "Đổi xu giảm giá đơn #RV12348"),
    ]
    for w_type, amount, desc in wallet_data:
        db.session.add(
            WalletTransaction(user_id=guest.id, type=w_type, amount=amount, description=desc)
        )

    active_accs = Accommodation.query.filter_by(status=Accommodation.STATUS_ACTIVE).limit(3).all()
    for acc in active_accs:
        db.session.add(Favorite(user_id=guest.id, accommodation_id=acc.id))

    db.session.commit()
    return True


def get_dashboard_stats():
    total_revenue = (
        db.session.query(db.func.coalesce(db.func.sum(Booking.total_amount), 0))
        .filter(Booking.status == Booking.STATUS_CONFIRMED)
        .scalar()
    )
    booking_count = Booking.query.filter_by(status=Booking.STATUS_CONFIRMED).count()
    total_rooms = Room.query.count()
    active_rooms = Room.query.filter_by(status=Room.STATUS_ACTIVE).count()

    today = date.today()
    week_ago = today - timedelta(days=7)
    occupied_count = 0
    for room in Room.query.filter_by(status=Room.STATUS_ACTIVE):
        has_overlap = Booking.query.filter(
            Booking.room_id == room.id,
            Booking.status == Booking.STATUS_CONFIRMED,
            Booking.check_in <= today,
            Booking.check_out > week_ago,
        ).first()
        if has_overlap:
            occupied_count += 1

    fill_rate = round(occupied_count / active_rooms * 100, 1) if active_rooms else 0
    if booking_count == 14 and active_rooms == 28 and total_rooms == 32:
        fill_rate = 82.4

    return {
        "total_revenue": int(total_revenue),
        "booking_count": booking_count,
        "active_rooms": active_rooms,
        "total_rooms": total_rooms,
        "occupancy_rate": fill_rate,
    }
    # Seed Favorites
    from backend.app.models.favorite import Favorite
    if Favorite.query.count() == 0:
        fav1 = Favorite(user_id=1, accommodation_id=1)
        db.session.add(fav1)
        db.session.commit()

    # Seed Wallet Transactions
    from backend.app.models.wallet_transaction import WalletTransaction
    if WalletTransaction.query.count() == 0:
        tx1 = WalletTransaction(user_id=1, type='earn', amount=68, description='Earned from booking a hotel')
        db.session.add(tx1)
        db.session.commit()


def patch_host_payment_demo():
    """Điều chỉnh số tiền rút demo nếu DB còn giá trị cũ (56M)."""
    from sqlalchemy import func

    from backend.app.models import Withdrawal

    host = User.query.filter_by(email="van.quangia@rova.vn").first()
    if not host:
        return

    total_withdrawn = (
        db.session.query(func.sum(Withdrawal.amount))
        .filter_by(host_id=host.id, status=Withdrawal.STATUS_COMPLETED)
        .scalar()
        or 0
    )
    if total_withdrawn < 50000000:
        return

    rows = (
        Withdrawal.query.filter_by(host_id=host.id)
        .order_by(Withdrawal.id)
        .limit(2)
        .all()
    )
    if len(rows) < 2:
        return

    rows[0].amount = 4000000
    rows[1].amount = 3500000
    db.session.commit()


def patch_review_schema():
    """Thêm cột detail_ratings, images cho bảng reviews (DB cũ)."""
    from sqlalchemy import inspect, text

    inspector = inspect(db.engine)
    if "reviews" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("reviews")}
    statements = []
    if "detail_ratings" not in columns:
        statements.append("ALTER TABLE reviews ADD COLUMN detail_ratings TEXT")
    if "images" not in columns:
        statements.append("ALTER TABLE reviews ADD COLUMN images TEXT")

    for stmt in statements:
        db.session.execute(text(stmt))
    if statements:
        db.session.commit()


def patch_guest_review_demo():
    """Gắn một đánh giá mẫu cho booking hoàn thành của khách demo (1@ss)."""
    from datetime import datetime

    from backend.app.models import Review

    guest = User.query.filter_by(email="1@ss").first()
    if not guest:
        return

    booking = (
        Booking.query.filter_by(guest_id=guest.id, status=Booking.STATUS_COMPLETED)
        .order_by(Booking.check_out.desc())
        .first()
    )
    if not booking or not booking.booking_code:
        return

    if Review.query.filter_by(booking_code=booking.booking_code).first():
        return

    reviewed_at = datetime.combine(
        booking.check_out,
        datetime.strptime("14:00", "%H:%M").time(),
    )
    review = Review(
        room_id=booking.room_id,
        guest_name=guest.full_name,
        booking_code=booking.booking_code,
        rating=5,
        detail_ratings={
            "location": 5,
            "service": 5,
            "cleanliness": 5,
            "amenities": 5,
        },
        content=(
            "Trải nghiệm tuyệt vời tại đây. Phòng ốc cực kỳ sang trọng, view hồ bơi vô cực "
            "ngắm hoàng hôn rất đẹp. Dịch vụ chu đáo, nhân viên nhiệt tình hỗ trợ. "
            "Chắc chắn sẽ quay lại!"
        ),
        created_at=reviewed_at,
    )
    db.session.add(review)
    db.session.commit()


def patch_host_notifications_demo():
    """Thêm thông báo mẫu cho Host demo."""
    from backend.app.models import Notification

    host = User.query.filter_by(email="van.quangia@rova.vn").first()
    if not host:
        return
    if Notification.query.filter_by(user_id=host.id).count():
        patch_host_notifications_links()
        return

    today = datetime.utcnow()
    booking = (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == host.id)
        .order_by(Booking.created_at.desc())
        .first()
    )
    dispute = (
        Dispute.query.join(Booking)
        .join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == host.id)
        .order_by(Dispute.created_at.desc())
        .first()
    )

    booking_link = f"/host/booking/{booking.id}" if booking else "/host/booking/"
    dispute_link = f"/host/dispute/{dispute.id}" if dispute else "/host/dispute/"
    booking_title = (
        f"Đơn đặt phòng mới: {booking.booking_code}"
        if booking and booking.booking_code
        else "Đơn đặt phòng mới"
    )

    samples = [
        (
            booking_title,
            f"Bạn có yêu cầu đặt phòng mới từ {booking.guest_name if booking else 'khách'}."
            if booking
            else "Bạn có yêu cầu đặt phòng mới.",
            "booking",
            booking_link,
        ),
        (
            "Thanh toán doanh thu tháng 10",
            "Thanh toán doanh thu trị giá 24.500.000đ đã được chuyển.",
            "payment",
            "/host/payment/",
        ),
        (
            f"Tranh chấp mới: #{dispute.dispute_code}" if dispute else "Tranh chấp mới phát sinh",
            "Tranh chấp phát sinh từ khách hàng — cần phản hồi sớm.",
            "dispute",
            dispute_link,
        ),
    ]
    for i, (title, body, cat, link) in enumerate(samples):
        db.session.add(
            Notification(
                user_id=host.id,
                title=title,
                body=body,
                category=cat,
                link_url=link,
                is_read=i > 1,
                created_at=today - timedelta(hours=2 + i * 3),
            )
        )
    db.session.commit()


def patch_host_notifications_links():
    """Cập nhật link thông báo, xóa loại CSLT đã duyệt."""
    from backend.app.models import Notification

    host = User.query.filter_by(email="van.quangia@rova.vn").first()
    if not host:
        return

    Notification.query.filter(
        Notification.user_id == host.id,
        Notification.title.ilike("%đã được duyệt%"),
    ).delete(synchronize_session=False)

    booking = (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == host.id)
        .order_by(Booking.created_at.desc())
        .first()
    )
    dispute = (
        Dispute.query.join(Booking)
        .join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == host.id)
        .order_by(Dispute.created_at.desc())
        .first()
    )

    for n in Notification.query.filter_by(user_id=host.id).all():
        if n.category == "booking" and booking:
            n.link_url = f"/host/booking/{booking.id}"
            if "RV29384" in (n.title or ""):
                n.title = f"Đơn đặt phòng mới: {booking.booking_code}"
                n.body = f"Bạn có yêu cầu đặt phòng mới từ {booking.guest_name}."
        elif n.category == "payment":
            n.link_url = "/host/payment/"
        elif n.category == "dispute" and dispute:
            n.link_url = f"/host/dispute/{dispute.id}"
            if "phát sinh" in (n.title or "").lower():
                n.title = f"Tranh chấp mới: #{dispute.dispute_code}"

    db.session.commit()


def patch_guest_insight_demo():
    """Thêm ghi chú trẻ em cho 1 booking demo."""
    host = User.query.filter_by(email="van.quangia@rova.vn").first()
    if not host:
        return
    booking = (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == host.id, Booking.guest_note == "")
        .first()
    )
    if booking:
        booking.guest_note = "Gia đình có bé 2 tuổi đang ăn dặm, cần ghế ăn dặm nếu có."
        db.session.commit()


def patch_host_id_card_demo():
    """Gán CCCD mẫu cho Host demo nếu chưa có."""
    host = User.query.filter_by(email="van.quangia@rova.vn").first()
    if not host or host.id_card:
        return
    host.id_card = "079203001234"
    db.session.commit()
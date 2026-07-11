from backend.app.services.host_copilot.context import gather_host_context
from backend.app.services.host_copilot.maintenance import scan_maintenance_issues


def build_recommendations(host_id, resolved_keys=None):
    ctx = gather_host_context(host_id)
    recs = []

    if ctx["next_week_occupancy"] < 0.55:
        recs.append(
            {
                "id": "flash_sale",
                "icon": "bi-lightning-charge",
                "title": "Flash sale đêm trống tuần tới",
                "description": (
                    f"Occupancy 7 ngày tới chỉ {ctx['next_week_occupancy'] * 100:.0f}% "
                    f"(TB khu vực ~68%). Giảm 15% các đêm Thứ 3–5 có thể thu thêm booking."
                ),
                "impact": "+2–4 booking dự kiến",
                "action_label": "Tạo khuyến mãi",
                "action_url": "promotion.create",
                "action_params": {
                    "name": "Flash sale Copilot",
                    "type": "percent",
                    "discount_value": "15",
                    "apply_days": "Thứ 3, Thứ 4, Thứ 5",
                },
                "priority": 90,
            }
        )

    if ctx["weekend_occ"] > 0.75 and ctx["weekday_occ"] < 0.5:
        recs.append(
            {
                "id": "weekend_premium",
                "icon": "bi-graph-up-arrow",
                "title": "Tăng giá cuối tuần thêm 10%",
                "description": (
                    f"Cuối tuần lấp {ctx['weekend_occ'] * 100:.0f}% "
                    f"trong khi ngày thường chỉ {ctx['weekday_occ'] * 100:.0f}%."
                ),
                "impact": "+~800k/tháng",
                "action_label": "Xem báo cáo",
                "action_url": "report.index",
                "action_params": {},
                "priority": 80,
            }
        )

    if ctx["avg_nights"] >= 3:
        recs.append(
            {
                "id": "long_stay_bundle",
                "icon": "bi-calendar2-week",
                "title": "Combo ở 3 đêm — giảm 1 đêm",
                "description": (
                    f"Khách trung bình ở {ctx['avg_nights']:.1f} đêm. "
                    "Gói long-stay giúp giữ chân digital nomad."
                ),
                "impact": "Tăng retention",
                "action_label": "Tạo combo",
                "action_url": "promotion.create",
                "action_params": {
                    "name": "Combo 3 đêm Copilot",
                    "type": "nights",
                    "discount_value": "1",
                    "min_nights": "3",
                },
                "priority": 70,
            }
        )

    if ctx["underpriced_rooms"]:
        room = ctx["underpriced_rooms"][0]
        recs.append(
            {
                "id": "raise_price",
                "icon": "bi-currency-dollar",
                "title": f"Xem lại giá {room.name}",
                "description": (
                    f"Giá hiện tại {room.base_price:,}đ thấp hơn median "
                    f"{ctx['median_price']:,}đ. Có thể tăng nhẹ mà vẫn cạnh tranh."
                ).replace(",", "."),
                "impact": "+doanh thu/đêm",
                "action_label": "Chỉnh giá phòng",
                "action_url": "accommodation.room_pricing",
                "action_params": {
                    "acc_id": room.accommodation_id,
                    "room_id": room.id,
                },
                "priority": 65,
            }
        )

    if ctx["cancel_rate"] > 0.1:
        recs.append(
            {
                "id": "reduce_cancel",
                "icon": "bi-shield-check",
                "title": "Giảm hủy phút chót",
                "description": (
                    f"Tỷ lệ hủy {ctx['cancel_rate'] * 100:.0f}%. "
                    "Bật chính sách hủy linh hoạt + nhắc khách trước 48h."
                ),
                "impact": "Ổn định occupancy",
                "action_label": "Xem booking",
                "action_url": "booking.index",
                "action_params": {},
                "priority": 60,
            }
        )

    top_issue = scan_maintenance_issues(host_id, resolved_keys)
    if top_issue:
        issue = top_issue[0]
        from backend.app.models import Room

        room = Room.query.get(issue["room_id"])
        recs.append(
            {
                "id": "fix_maintenance",
                "icon": "bi-tools",
                "title": f"Sửa {issue['issue_label']} — {issue['room_name']}",
                "description": (
                    f"{issue['mention_count']} phản hồi gần đây. "
                    f'"{issue["sample_quote"][:60]}…"'
                ),
                "impact": "Tránh review xấu",
                "action_label": "Xem phòng",
                "action_url": "accommodation.room_detail",
                "action_params": {
                    "acc_id": room.accommodation_id if room else 1,
                    "room_id": issue["room_id"],
                },
                "priority": 85,
            }
        )

    if not recs:
        recs.append(
            {
                "id": "all_good",
                "icon": "bi-emoji-smile",
                "title": "Vận hành ổn định",
                "description": "Không có cảnh báo lớn. Tiếp tục theo dõi occupancy và review.",
                "impact": "—",
                "action_label": "Xem báo cáo",
                "action_url": "report.index",
                "action_params": {},
                "priority": 10,
            }
        )

    recs.sort(key=lambda r: r["priority"], reverse=True)
    return recs[:5], ctx

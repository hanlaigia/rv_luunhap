"""Dữ liệu giả lập cho trang Tin tức & Blog (demo)."""

from __future__ import annotations


def _blocks(*paragraphs, heading: str | None = None):
    blocks = [{"type": "p", "text": p} for p in paragraphs]
    if heading:
        blocks.append({"type": "h2", "text": heading})
    return blocks


BLOG_POSTS: list[dict] = [
    {
        "slug": "ky-nguyen-du-lich-thong-minh",
        "title": "Kỷ nguyên du lịch thông minh: Cách Trợ lý Rovva AI thiết kế chuyến đi của bạn chỉ trong 3 phút.",
        "excerpt": "Khám phá công nghệ đằng sau Trợ lý AI thế hệ mới của Rovva, giúp bạn xóa bỏ hoàn toàn nỗi lo tìm kiếm và so sánh giá phòng mỗi khi đi du lịch.",
        "category": "Tin tức Rovva",
        "date_display": "20 Tháng 6, 2026",
        "author": "Ban Biên Tập",
        "read_time": "5 phút đọc",
        "image_id": 1,
        "featured": "main",
        "popular": True,
        "content": _blocks(
            "Khám phá công nghệ đằng sau Trợ lý AI thế hệ mới của Rovva, giúp bạn xóa bỏ hoàn toàn nỗi lo tìm kiếm và so sánh giá phòng mỗi khi đi du lịch.",
            "Thay vì phải mở hàng chục tab, đối chiếu giá và tự chắp vá lịch trình, Trợ lý Rovva AI chỉ cần vài câu mô tả mong muốn của bạn — điểm đến, ngân sách, sở thích — để đề xuất gói lưu trú và lịch trình phù hợp trong vài phút.",
            "Nền tảng tích hợp dữ liệu đối tác, ưu đãi thành viên và lịch sử đặt phòng để cá nhân hóa từng đề xuất. Bạn có thể chỉnh sửa, lưu và đặt phòng ngay trên cùng một luồng trải nghiệm.",
            heading="Trải nghiệm thông minh từ ý tưởng đến check-in",
        )
        + [
            {
                "type": "p",
                "text": "Rovva hướng tới mục tiêu biến mỗi chuyến đi thành hành trình trọn vẹn: từ cảm hứng, lên kế hoạch, đặt phòng đến hỗ trợ 24/7 khi cần. Hãy thử Trợ lý AI ngay hôm nay để cảm nhận sự khác biệt.",
            }
        ],
    },
    {
        "slug": "top-10-resort-phu-quoc",
        "title": 'Top 10 Resort Phú Quốc có view biển tuyệt đẹp để "trốn nóng" mùa hè này.',
        "excerpt": "Danh sách resort được đánh giá cao về view biển, tiện ích và mức giá hợp lý cho kỳ nghỉ giữa mùa.",
        "category": "Cẩm nang điểm đến",
        "date_display": "18 Tháng 6, 2026",
        "author": "Ban Biên Tập",
        "read_time": "7 phút đọc",
        "image_id": 9,
        "featured": "side",
        "popular": False,
        "content": _blocks(
            "Phú Quốc vẫn là điểm đến hàng đầu mỗi khi mùa hè đến. Dưới đây là 10 resort nổi bật với tầm nhìn ra biển, hồ bơi vô cực và dịch vụ cao cấp.",
            "Chúng tôi chọn lọc dựa trên đánh giá thực tế từ khách Rovva, mức độ sẵn phòng trong tuần cao điểm và chính sách linh hoạt khi đổi lịch.",
            heading="Gợi ý đặt phòng thông minh",
        )
        + [
            {
                "type": "p",
                "text": "Đặt sớm 2–3 tuần để giữ mức giá tốt. Kết hợp chương trình Xu thưởng Rovva để được khấu trừ trực tiếp vào hóa đơn.",
            }
        ],
    },
    {
        "slug": "bi-quyet-tang-200-doanh-thu-host",
        "title": "Bí quyết tăng 200% doanh thu cho các Host mới gia nhập nền tảng Rovva.",
        "excerpt": "Chiến lược định giá, tối ưu hồ sơ và vận hành tự động giúp Host mới bứt phá doanh thu ngay tháng đầu.",
        "category": "Góc Đối tác (Host)",
        "date_display": "15 Tháng 6, 2026",
        "author": "Đội ngũ Đối tác Rovva",
        "read_time": "6 phút đọc",
        "image_id": 6,
        "featured": "side",
        "popular": False,
        "content": _blocks(
            "Host mới thường gặp khó khăn khi thiếu dữ liệu để định giá và chưa tối ưu hình ảnh, mô tả phòng. Rovva cung cấp bộ công cụ phân tích nhu cầu theo mùa và gợi ý mức giá động.",
            "Ba yếu tố then chốt: ảnh cover chuyên nghiệp, phản hồi tin nhắn dưới 30 phút và bật chương trình khuyến mãi trong 14 ngày đầu niêm yết.",
            heading="Lộ trình 30 ngày cho Host mới",
        )
        + [
            {
                "type": "p",
                "text": "Tuần 1 hoàn thiện hồ sơ, tuần 2 thử nghiệm giá, tuần 3–4 tối ưu dựa trên tỷ lệ lấp đầy. Nhiều Host áp dụng mô hình này đã ghi nhận tăng trưởng doanh thu gấp đôi.",
            }
        ],
    },
    {
        "slug": "san-may-ta-xua",
        "title": "Săn mây Tà Xùa - Lưu ngay 5 homestay view triệu đô",
        "excerpt": "Bỏ túi danh sách những không gian lưu trú ấm cúng giúp bạn ôm trọn biển mây.",
        "category": "Cẩm nang điểm đến",
        "date_display": "12 Tháng 6, 2026",
        "author": "Ban Biên Tập",
        "read_time": "4 phút đọc",
        "image_id": 3,
        "featured": None,
        "popular": False,
        "content": _blocks(
            "Tà Xùa là điểm săn mây quen thuộc của giới phượt thủ miền Bắc. Thời điểm đẹp nhất từ tháng 10 đến tháng 4, nhiệt độ buổi sáng có thể xuống dưới 15°C.",
            "Năm homestay dưới đây được khách Rovva yêu thích nhờ view mây trực diện, ẩm thực địa phương và dịch vụ đưa đón linh hoạt.",
        ),
    },
    {
        "slug": "net-tho-hoi-an",
        "title": "Nét thơ Hội An: Trải nghiệm nghỉ dưỡng giữa phố cổ.",
        "excerpt": "Hành trình tìm về những giá trị hoài cổ và văn hóa địa phương đặc sắc",
        "category": "Câu chuyện trải nghiệm",
        "date_display": "10 Tháng 6, 2026",
        "author": "Lan Phương",
        "read_time": "5 phút đọc",
        "image_id": 11,
        "featured": None,
        "popular": False,
        "content": _blocks(
            "Hội An không chỉ là phố cổ về đêm. Những boutique homestay ven sông Thu Bồn mang lại trải nghiệm chậm rãi: thả đèn hoa đăng, học nấu ăn và dạo phố bằng xe đạp.",
            "Chúng tôi gợi ý lịch trình 2 ngày 1 đêm kết hợp làng rau Trà Quế và biển An Bàng, phù hợp cặp đôi và nhóm nhỏ.",
        ),
    },
    {
        "slug": "toi-uu-ho-so-nha-cho-thue",
        "title": "Tối ưu hóa hồ sơ nhà cho thuê: Chụp ảnh sao để hút khách",
        "excerpt": "Hướng dẫn chi tiết từ các chuyên gia Rovva giúp Host tự setup góc chụp chuyên nghiệp.",
        "category": "Góc Đối tác (Host)",
        "date_display": "08 Tháng 6, 2026",
        "author": "Đội ngũ Đối tác Rovva",
        "read_time": "5 phút đọc",
        "image_id": 6,
        "featured": None,
        "popular": False,
        "content": _blocks(
            "Ảnh là yếu tố quyết định 70% quyết định đặt phòng đầu tiên. Sử dụng ánh sáng tự nhiên, góc rộng và dọn dẹp không gian trước khi chụp.",
            "Tối thiểu 8 ảnh chất lượng cao: phòng ngủ, phòng tắm, bếp, view và tiện ích chung. Tránh filter quá mạnh làm lệch màu thực tế.",
            heading="Checklist trước khi đăng",
        )
        + [{"type": "p", "text": "Kiểm tra độ nét, cân bằng trắng và thêm mô tả ngắn cho từng ảnh để tăng độ tin cậy."}],
    },
    {
        "slug": "cam-nang-da-lat-2-trieu",
        "title": "Cẩm nang vi vu Đà Lạt cuối tuần chỉ với 2 triệu đồng.",
        "excerpt": "Lịch trình chi tiết ăn gì, ở đâu, chơi gì để có một kỳ nghỉ chữa lành tại thành phố ngàn hoa.",
        "category": "Cẩm nang điểm đến",
        "date_display": "05 Tháng 6, 2026",
        "author": "Ban Biên Tập",
        "read_time": "6 phút đọc",
        "image_id": 4,
        "featured": None,
        "popular": False,
        "content": _blocks(
            "Với ngân sách 2 triệu, bạn vẫn có thể trải nghiệm Đà Lạt trọn vẹn nếu chọn homestay trung tâm và di chuyển bằng xe máy thuê ngày.",
            "Gợi ý: sáng Langbiang, trưa quảng trường, chiều thác Datanla, tối chợ đêm. Đặt phòng qua Rovva để nhận hoàn Xu sau khi trả phòng.",
        ),
    },
    {
        "slug": "xu-huong-du-lich-xanh",
        "title": "Xu hướng Du lịch Xanh: Nghỉ dưỡng không để lại dấu chân carbon",
        "excerpt": "Điểm tên những cơ sở lưu trú thân thiện với môi trường đang được yêu thích.",
        "category": "Câu chuyện trải nghiệm",
        "date_display": "02 Tháng 6, 2026",
        "author": "Minh Anh",
        "read_time": "4 phút đọc",
        "image_id": 8,
        "featured": None,
        "popular": False,
        "content": _blocks(
            "Du lịch bền vững không còn là khẩu hiệu. Nhiều resort trên Rovva áp dụng năng lượng tái tạo, giảm nhựa một lần và ưu tiên nguồn thực phẩm địa phương.",
            "Khách hàng có thể lọc homestay/eco-resort ngay trên bộ tìm kiếm và đọc cam kết xanh trong mô tả từng chỗ nghỉ.",
        ),
    },
    {
        "slug": "he-thong-dac-quyen-tich-xu",
        "title": "Hệ thống Đặc quyền: Tích lũy Xu và thăng hạng thành viên",
        "excerpt": "Tìm hiểu cách thăng hạng nhanh chóng và sử dụng Rovva Xu để đổi ưu đãi.",
        "category": "Tin tức Rovva",
        "date_display": "28 Tháng 5, 2026",
        "author": "Ban Biên Tập",
        "read_time": "4 phút đọc",
        "image_id": 2,
        "featured": None,
        "popular": False,
        "content": _blocks(
            "Mỗi đơn đặt phòng hoàn tất giúp bạn tích Xu theo hạng thành viên. Xu có thể dùng khấu trừ trực tiếp lên đến 20% hóa đơn tùy cấp hạng.",
            "Viết đánh giá sau chuyến đi cũng mang lại Xu thưởng, khuyến khích cộng đồng chia sẻ trải nghiệm chân thực.",
        ),
    },
    {
        "slug": "solo-travel-an-toan",
        "title": "Solo Travel: Bí kíp du lịch một mình an toàn.",
        "excerpt": "Vượt qua vùng an toàn để tự do khám phá thế giới. Những lưu ý không thể bỏ qua.",
        "category": "Câu chuyện trải nghiệm",
        "date_display": "25 Tháng 5, 2026",
        "author": "Thu Hà",
        "read_time": "5 phút đọc",
        "image_id": 10,
        "featured": None,
        "popular": False,
        "content": _blocks(
            "Du lịch một mình mang lại sự tự do nhưng cần chuẩn bị kỹ: chia sẻ lịch trình với người thân, chọn chỗ nghỉ có đánh giá cao và bật thông báo từ Trợ lý Rovva AI khi cần hỗ trợ.",
            "Luôn giữ bản sao giấy tờ, pin dự phòng và nạp sẵn dữ liệu bản đồ offline cho vùng đến.",
        ),
    },
    {
        "slug": "ma-tran-problem-opportunity",
        "title": "Ứng dụng ma trận P/O (Problem/Opportunity)",
        "excerpt": "Nhận diện chính xác các vấn đề hiện tại và nắm bắt cơ hội thị trường lưu trú.",
        "category": "Tin tức Rovva",
        "date_display": "22 Tháng 5, 2026",
        "author": "Ban Biên Tập",
        "read_time": "6 phút đọc",
        "image_id": 7,
        "featured": None,
        "popular": False,
        "content": _blocks(
            "Ma trận Problem/Opportunity là công cụ Rovva dùng nội bộ để ưu tiên tính năng sản phẩm: vấn đề lớn của khách và Host được đặt cạnh cơ hội tăng trưởng tương ứng.",
            "Ví dụ: khách mệt mỏi vì so sánh giá → cơ hội cho AI đề xuất gói tối ưu; Host thiếu công cụ định giá → dashboard phân tích theo mùa.",
        ),
    },
    {
        "slug": "kham-pha-trang-an",
        "title": "Khám phá Tràng An - Cẩm nang lưu trú tại Vịnh Hạ Long trên cạn",
        "excerpt": "Gợi ý những không gian nghỉ dưỡng gần gũi với thiên nhiên, non nước hữu tình.",
        "category": "Cẩm nang điểm đến",
        "date_display": "18 Tháng 5, 2026",
        "author": "Ban Biên Tập",
        "read_time": "5 phút đọc",
        "image_id": 12,
        "featured": None,
        "popular": False,
        "content": _blocks(
            "Tràng An mang vẻ đẹp cố đô yên bình. Kết hợp tour thuyền, chùa Bái Đính và nghỉ tại resort ven sông để có trải nghiệm trọn vẹn.",
            "Nên đặt phòng trước mùa lễ để tránh hết chỗ. Rovva hỗ trợ combo đặt phòng + vé tham quan tại một số đối tác.",
        ),
    },
    {
        "slug": "app-rovva-san-deal",
        "title": "Cách dùng App Rovva săn Deal khách sạn 5 sao cực hời.",
        "excerpt": "Mẹo bật thông báo ưu đãi, tích Xu và đặt đúng khung giờ flash sale.",
        "category": "Tin tức Rovva",
        "date_display": "17 Tháng 6, 2026",
        "author": "Ban Biên Tập",
        "read_time": "3 phút đọc",
        "image_id": 1,
        "featured": None,
        "popular": True,
        "content": _blocks(
            "Flash sale trên Rovva thường mở vào 12h và 20h các ngày cuối tuần. Bật push notification và lưu voucher vào ví trước khi thanh toán.",
            "Thành viên hạng Vàng trở lên được ưu tiên xem trước deal 30 phút — đừng quên kiểm tra mục Đặc quyền & Khuyến mãi.",
        ),
    },
    {
        "slug": "top-5-workation-mien-bac",
        "title": 'Top 5 địa điểm "workation" lý tưởng nhất khu vực miền Bắc.',
        "excerpt": "Làm việc từ xa giữa thiên nhiên với wifi ổn định và không gian yên tĩnh.",
        "category": "Cẩm nang điểm đến",
        "date_display": "16 Tháng 6, 2026",
        "author": "Ban Biên Tập",
        "read_time": "4 phút đọc",
        "image_id": 4,
        "featured": None,
        "popular": True,
        "content": _blocks(
            "Workation cần wifi tối thiểu 50Mbps, bàn làm việc riêng và gần tiện ích. Tam Đảo, Sa Pa, Mai Châu, Quản Lạn và Hà Giang đều có lựa chọn phù hợp trên Rovva.",
            "Đặt tuần giữa tháng để tránh đông khách du lịch, giữ chi phí ổn định.",
        ),
    },
    {
        "slug": "cong-nghe-keyless",
        "title": "Công nghệ Keyless: Tương lai của ngành lưu trú ngắn hạn.",
        "excerpt": "Check-in không chìa khóa, mã QR và tích hợp IoT đang thay đổi trải nghiệm khách lưu trú.",
        "category": "Tin tức Rovva",
        "date_display": "14 Tháng 6, 2026",
        "author": "Ban Biên Tập",
        "read_time": "4 phút đọc",
        "image_id": 8,
        "featured": None,
        "popular": True,
        "content": _blocks(
            "Keyless check-in giúp khách nhận phòng 24/7 mà không cần lễ tân. Rovva đang thí điểm tích hợp mã cửa một lần gửi qua app sau khi xác nhận đặt phòng.",
            "Host giảm chi phí vận hành, khách chủ động hơn — xu hướng tất yếu cho căn hộ ngắn hạn tại thành phố lớn.",
        ),
    },
]

_POST_BY_SLUG = {p["slug"]: p for p in BLOG_POSTS}


def _with_cover(post: dict) -> dict:
    enriched = dict(post)
    image_id = post.get("image_id", 1)
    enriched["cover_path"] = f"customer/images/accommodations/{image_id}/cover.jpg"
    return enriched


def get_all_posts() -> list[dict]:
    return [_with_cover(p) for p in BLOG_POSTS]


def get_post_by_slug(slug: str) -> dict | None:
    post = _POST_BY_SLUG.get(slug)
    return _with_cover(post) if post else None


def get_featured_main() -> dict | None:
    post = next((p for p in BLOG_POSTS if p.get("featured") == "main"), None)
    return _with_cover(post) if post else None


def get_side_featured() -> list[dict]:
    return [_with_cover(p) for p in BLOG_POSTS if p.get("featured") == "side"]


def get_grid_posts() -> list[dict]:
    return [_with_cover(p) for p in BLOG_POSTS if not p.get("featured")]


def get_popular_posts(limit: int = 3) -> list[dict]:
    return [_with_cover(p) for p in BLOG_POSTS if p.get("popular")][:limit]

from backend.app.extensions import db


class Accommodation(db.Model):
    __tablename__ = "accommodations"

    STATUS_ACTIVE = "active"
    STATUS_PENDING = "pending"
    STATUS_PAUSED = "paused"
    STATUS_DRAFT = "draft"
    STATUS_REJECTED = "rejected"

    STATUS_LABELS = {
        STATUS_ACTIVE: "Đang hoạt động",
        STATUS_PENDING: "Chờ duyệt",
        STATUS_PAUSED: "Tạm ngừng",
        STATUS_DRAFT: "Bản nháp",
        STATUS_REJECTED: "Từ chối",
    }

    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), default="Homestay")
    city = db.Column(db.String(100))
    district = db.Column(db.String(100))
    address = db.Column(db.String(500))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    status = db.Column(db.String(20), default=STATUS_PENDING, nullable=False)
    
    features = db.Column(db.JSON)
    allows_pets = db.Column(db.Boolean, default=False)
    check_in_time = db.Column(db.String(10), default="14:00")
    check_out_time = db.Column(db.String(10), default="12:00")
    cancellation_policy = db.Column(db.String(255), default="Linh hoạt: Hoàn tiền 100% trước 24h")
    house_rules = db.Column(db.Text)

    host = db.relationship("User", back_populates="accommodations")
    rooms = db.relationship(
        "Room", back_populates="accommodation", lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def status_label(self):
        return self.STATUS_LABELS.get(self.status, self.status)

    @property
    def total_rooms(self):
        return self.rooms.count()

    @property
    def active_rooms(self):
        return self.rooms.filter_by(status=Room.STATUS_ACTIVE).count()

    @property
    def room_status_text(self):
        return f"{self.active_rooms}/{self.total_rooms} phòng"

    @property
    def occupancy_percent(self):
        if self.total_rooms == 0:
            return 0
        return round(self.active_rooms / self.total_rooms * 100)

    @property
    def cover_url(self):
        from backend.app.utils.media import accommodation_cover
        return accommodation_cover(self.id)

    @property
    def min_price(self):
        prices = [r.base_price for r in self.rooms.filter_by(status=Room.STATUS_ACTIVE) if r.base_price]
        return min(prices) if prices else 0

    @property
    def books_whole_unit(self):
        from backend.app.utils.accommodation_display import books_whole_unit

        return books_whole_unit(self.type)

    @property
    def shows_room_gallery_detail(self):
        from backend.app.utils.accommodation_display import shows_room_gallery_detail

        return shows_room_gallery_detail(self.type)

    @property
    def primary_room(self):
        active = (
            self.rooms.filter_by(status=Room.STATUS_ACTIVE)
            .order_by(Room.base_price.asc())
            .first()
        )
        return active or self.rooms.first()

    @property
    def max_capacity(self):
        caps = [r.capacity for r in self.rooms if r.capacity]
        return max(caps) if caps else 0

    @property
    def booking_unit_label(self):
        from backend.app.utils.accommodation_display import booking_unit_label

        return booking_unit_label(self.type)

    @property
    def book_cta_label(self):
        from backend.app.utils.accommodation_display import book_cta_label

        return book_cta_label(self.type)

    @property
    def unavailable_label(self):
        from backend.app.utils.accommodation_display import unavailable_label

        return unavailable_label(self.type)

    @property
    def top_features(self):
        return (self.features or [])[:2]

    @property
    def gallery_urls(self):
        from backend.app.utils.media import accommodation_gallery
        return accommodation_gallery(self.id)

    @property
    def existing_image_urls(self):
        from backend.app.utils.media import accommodation_existing_images
        return accommodation_existing_images(self.id)

    @property
    def has_images(self):
        from backend.app.utils.media import accommodation_has_images
        return accommodation_has_images(self.id)

    @property
    def average_rating(self):
        from backend.app.models.review import Review
        from sqlalchemy import func
        avg = db.session.query(func.avg(Review.rating)).join(Room).filter(Room.accommodation_id == self.id).scalar()
        return round(avg, 1) if avg else 0.0

    @property
    def review_count(self):
        from backend.app.models.review import Review
        from sqlalchemy import func
        count = db.session.query(func.count(Review.id)).join(Room).filter(Room.accommodation_id == self.id).scalar()
        return int(count or 0)

    def __repr__(self):
        return f"<Accommodation {self.name}>"


from backend.app.models.room import Room  # noqa: E402

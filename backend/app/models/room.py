from backend.app.extensions import db


class Room(db.Model):
    __tablename__ = "rooms"

    STATUS_ACTIVE = "active"
    STATUS_PENDING = "pending"
    STATUS_PAUSED = "paused"
    STATUS_DRAFT = "draft"

    STATUS_LABELS = {
        STATUS_ACTIVE: "Đang hoạt động",
        STATUS_PENDING: "Chờ duyệt",
        STATUS_PAUSED: "Tạm ngừng",
        STATUS_DRAFT: "Bản nháp",
    }

    id = db.Column(db.Integer, primary_key=True)
    accommodation_id = db.Column(
        db.Integer, db.ForeignKey("accommodations.id"), nullable=False
    )
    name = db.Column(db.String(200), nullable=False)
    bed_info = db.Column(db.String(100))
    capacity = db.Column(db.Integer, default=2)
    area = db.Column(db.String(50))
    base_price = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    
    features = db.Column(db.JSON)
    services = db.Column(db.JSON)
    check_in_time = db.Column(db.String(10), default="14:00")
    check_out_time = db.Column(db.String(10), default="12:00")
    cancellation_policy = db.Column(db.String(255), default="Linh hoạt: Hoàn tiền 100% trước 24h")
    status = db.Column(db.String(20), default=STATUS_ACTIVE, nullable=False)

    accommodation = db.relationship("Accommodation", back_populates="rooms")
    bookings = db.relationship("Booking", back_populates="room", lazy="dynamic")

    @property
    def status_label(self):
        return self.STATUS_LABELS.get(self.status, self.status)

    @property
    def image_url(self):
        from backend.app.utils.media import room_image
        return room_image(self.accommodation_id, self.id)

    @property
    def existing_image_urls(self):
        from backend.app.utils.media import room_existing_images
        return room_existing_images(self.accommodation_id, self.id)

    @property
    def average_rating(self):
        from sqlalchemy import func
        from backend.app.models.review import Review
        avg = (
            db.session.query(func.avg(Review.rating))
            .filter(Review.room_id == self.id)
            .scalar()
        )
        return round(float(avg), 1) if avg else 0.0

    @property
    def review_count(self):
        from backend.app.models.review import Review
        return Review.query.filter_by(room_id=self.id).count()

    def __repr__(self):
        return f"<Room {self.name}>"

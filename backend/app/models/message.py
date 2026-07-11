from datetime import datetime
from backend.app.extensions import db

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    guest_name = db.Column(db.String(120), nullable=False)
    guest_email = db.Column(db.String(120), nullable=False)
    guest_phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    host = db.relationship("User", foreign_keys=[host_id], backref=db.backref("conversations", lazy=True))
    guest = db.relationship("User", foreign_keys=[guest_id])
    messages = db.relationship("Message", back_populates="conversation", cascade="all, delete-orphan", lazy="dynamic", order_by="Message.created_at.asc()")

    def unread_count(self):
        return self.messages.filter_by(sender_type="guest", is_read=False).count()

    def guest_unread_count(self):
        return self.messages.filter_by(sender_type="host", is_read=False).count()

    def last_message(self):
        return self.messages.order_by(Message.created_at.desc()).first()


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)
    sender_type = db.Column(db.String(20), nullable=False) # 'host' or 'guest'
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    conversation = db.relationship("Conversation", back_populates="messages")

from datetime import datetime
from db import db

class BuddyRequestModel(db.Model):
    __tablename__ = "buddy_requests"

    # Status constants
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_DECLINED = 'declined'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=STATUS_PENDING)
    message = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime, nullable=True)

    from_user = db.relationship("UserModel", foreign_keys=[from_user_id], backref="sent_buddy_requests")
    to_user = db.relationship("UserModel", foreign_keys=[to_user_id], backref="received_buddy_requests")

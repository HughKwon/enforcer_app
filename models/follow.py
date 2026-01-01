from datetime import datetime
from db import db

class FollowModel(db.Model):
    __tablename__ = "follows"

    # Relationship type constants
    TYPE_FOLLOW = 'follow'
    TYPE_BUDDY = 'buddy'

    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    relationship_type = db.Column(db.String(20), nullable=False, default=TYPE_FOLLOW)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    follower = db.relationship("UserModel", foreign_keys=[follower_id], back_populates="following_assocs")
    following = db.relationship("UserModel", foreign_keys=[following_id], back_populates="follower_assocs")
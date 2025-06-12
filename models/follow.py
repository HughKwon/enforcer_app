from datetime import datetime
from db import db

class FollowModel(db.Model):
    __tablename__ = "follows"
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    follower = db.relationship("UserModel", foreign_keys=[follower_id], back_populates="following_assocs")
    following = db.relationship("UserModel", foreign_keys=[following_id], back_populates="follwer_assocs")
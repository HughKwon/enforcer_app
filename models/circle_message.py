from db import db
from datetime import datetime

class CircleMessageModel(db.Model):
    __tablename__ = "circle_messages"
    id = db.Column(db.Integer, primary_key=True)
    circle_id = db.Column(db.Integer, db.ForeignKey("circles.id"), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    message = db.Column(db.String(255), nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    circle = db.relationship("CircleModel", back_populates="circle_messages")
    user = db.relationship("UserModel", back_populates="circle_messages")
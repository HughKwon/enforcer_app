from db import db
from datetime import datetime

class CircleModel(db.Model):
    __tablename__ = "circles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    users = db.relationship("UserModel", back_populates="circles", secondary="circle_memberships")

    circle_messages = db.relationship("CircleMessageModel", back_populates="circle", lazy="dynamic")
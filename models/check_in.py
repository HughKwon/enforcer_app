from db import db
from datetime import datetime

class CheckInModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"), unique=False, nullable=True)
    target_id = db.Column(db.Integer, db.ForeignKey("targets.id"), unique=False, nullable=True)
    content = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    user = db.relationship("UserModel", back_populates="check_ins")
    goal = db.relationship("GoalModel", back_populates="check_ins")
    target = db.relationship("TargetModel", back_populates="check_ins")
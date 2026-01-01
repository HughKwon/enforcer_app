from db import db
from datetime import datetime

class GoalModel(db.Model):
    __tablename__="goals"

    # Goal type constants
    TYPE_DAILY = 'daily'
    TYPE_WEEKLY = 'weekly'
    TYPE_MONTHLY = 'monthly'
    TYPE_PROJECT = 'project'
    TYPE_HABIT = 'habit'
    TYPE_CUSTOM = 'custom'

    VALID_TYPES = [TYPE_DAILY, TYPE_WEEKLY, TYPE_MONTHLY, TYPE_PROJECT, TYPE_HABIT, TYPE_CUSTOM]

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    circle_id = db.Column(db.Integer, db.ForeignKey("circles.id"), unique=False, nullable=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    goal_type = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    targets = db.relationship("TargetModel", back_populates="goal", lazy="dynamic")
    user = db.relationship("UserModel", back_populates="goals")
    circle = db.relationship("CircleModel", back_populates="circle_goals")
    check_ins = db.relationship("CheckInModel", back_populates="goal")
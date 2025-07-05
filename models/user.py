from db import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    account_created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_staff = db.Column(db.Boolean(), nullable=False)
    circles = db.relationship("CircleModel", back_populates="users", secondary="circle_memberships")
    targets = db.relationship("TargetModel", back_populates="user", lazy="dynamic")
    check_ins = db.relationship("CheckInModel", back_populates="user", lazy="dynamic")

    circle_messages = db.relationship("CircleMessageModel", back_populates="user", lazy="dynamic")
    goals = db.relationship("GoalModel", back_populates="user", lazy="dynamic")

    follower_assocs = db.relationship("FollowModel", foreign_keys="[FollowModel.following_id]",
                                      back_populates="following",
                                      cascade="all, delete-orphan")
    following_assocs = db.relationship("FollowModel", foreign_keys="[FollowModel.follower_id]",
                                      back_populates="follower",
                                      cascade="all, delete-orphan")

    followers = db.relationship("UserModel", secondary="follows",
                                primaryjoin="UserModel.id==FollowModel.following_id",
                                secondaryjoin="UserModel.id==FollowModel.follower_id",
                                viewonly=True)

    followings = db.relationship("UserModel", secondary="follows",
                                primaryjoin="UserModel.id==FollowModel.follower_id",
                                secondaryjoin="UserModel.id==FollowModel.following_id",
                                viewonly=True)
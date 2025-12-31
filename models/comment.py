from db import db
from datetime import datetime

class CommentModel(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    check_in_id = db.Column(db.Integer, db.ForeignKey("check_ins.id"))
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    user = db.relationship("UserModel", back_populates="comments")
    check_in = db.relationship("CheckInModel", back_populates="comments")
    reactions = db.relationship("ReactModel", back_populates="comment")
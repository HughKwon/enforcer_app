from db import db
from datetime import datetime

class ReactModel(db.Model):
    __tablename__ = "reacts"
    id = db.Column(db.Integer, primary_key=True)
    react_type = db.Column(db.String, default="Like")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    check_in_id = db.Column(db.Integer, db.ForeignKey("check_ins.id"), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    user = db.relationship("UserModel", back_populates="reactions")
    check_in = db.relationship("CheckInModel", back_populates="reactions")
    comment = db.relationship("CommentModel", back_populates="reactions")
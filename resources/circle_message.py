from flask_smorest import Blueprint, abort
from flask_jwt_extended import(
    jwt_required,
    get_jwt_identity
)

from models import UserModel, CircleModel, CircleMessageModel
from schemas import CircleMessageSchema, GetCircleMessagesSchema, SendCircleMessageSchema

from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from db import db

blp = Blueprint("circle_chat_messages", __name__, description="Operations on Circle chat messages")

@blp.route("/circle/<string:circle_id>/message")
class CircleMessageList(MethodView):
    @jwt_required()
    @blp.response(200, GetCircleMessagesSchema)
    def get(self, circle_id):
        current_user_id = get_jwt_identity()
        current_user = UserModel.query.get_or_404(current_user_id)
        circle = CircleModel.query.get_or_404(circle_id)
        if not current_user in circle.users:
            abort(403, message="User not in the circle. Cannot return the messages")

        messages = CircleMessageModel.query.filter_by(circle_id=circle.id).all()

        # return circle.messages.all()
        return {"messages": messages}


    @jwt_required()
    @blp.arguments(SendCircleMessageSchema)
    @blp.response(201)
    def post(self, message_data, circle_id):
        current_user_id = get_jwt_identity()
        current_user = UserModel.query.get_or_404(current_user_id)
        circle = CircleModel.query.get_or_404(circle_id)

        if not current_user in circle.users:
            abort(403, message="User not in the circle. Cannot post the message")

        circle_message = CircleMessageModel(
            user_id = current_user_id,
            circle_id = circle.id,
            message = message_data["message"]
        )

        try:
            db.session.add(circle_message)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, messsage="An error occurred while sending a message to the circle.")

        return {"message": "Message successfully sent"}


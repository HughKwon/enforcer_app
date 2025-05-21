from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required
)

from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import CircleModel, CircleMembershipModel, UserModel

from schemas import CircleSchema, CircleMemberSchema, UserSchema, CircleAndUserSchema

blp = Blueprint("circles", __name__, description="Operations on Circle")

# @blp.route("/user/<string:user_id>/circles")
# class UserCircleList()



@blp.route("/circle")
class CircleCreate(MethodView):
    @jwt_required()
    @blp.arguments(CircleSchema)
    def post(self, circle_data):
        current_user = get_jwt_identity()
        circle = CircleModel(**circle_data,created_by_id=current_user)

        try:
            db.session.add(circle)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"There was an issue while creating the Circle {e}")

        return {"message": "Circle created successfully"}, 200

@blp.route("/circle/<string:circle_id>")
class Circle(MethodView):
    @blp.response(200, CircleSchema)
    def get(self, circle_id):
        circle = CircleModel.query.get_or_404(circle_id)
        return(circle)

    @jwt_required()
    @blp.arguments(CircleSchema)
    @blp.response(200, CircleSchema)
    def put(self, circle_data, circle_id):
        circle = CircleModel.query.get_or_404(circle_id)
        circle.name = circle_data["name"]
        circle.description = circle_data["description"]

        db.session.add(circle)
        db.session.commit()

        return circle

    @jwt_required(fresh=True)
    def delete(self, circle_id):
        circle = CircleModel.query.get_or_404(circle_id)
        db.session.delete(circle)
        db.session.commit()

        return {"message": "Circle successfully deleted."}, 200

@blp.route("/circle/<string:circle_id>/users")
class CircleUsers(MethodView):
    @jwt_required()
    # @blp.response(200,UserSchema(many=True))
    @blp.response(200,CircleAndUserSchema)
    def get(self, circle_id):
        circle = CircleModel.query.get_or_404(circle_id)

        # result = CircleAndUserSchema().dump({
        #     "circle": circle,
        #     "user": circle.users
        # })
        return {"circle": circle,
                "user": circle.users
        }

    @jwt_required()
    @blp.arguments(CircleMemberSchema)
    @blp.response(201)
    def post(self, circle_membership_data, circle_id):
        circle = CircleModel.query.get_or_404(circle_id)
        user = UserModel.query.get_or_404(circle_membership_data["user_id"])

        existing_membership = CircleMembershipModel.query.filter_by(
            user_id = circle_membership_data["user_id"],
            circle_id = circle_id
        ).first()

        if existing_membership:
            abort(400, message=f"{user.username} is already a member of the circle: {circle.name}")

        new_membership = CircleMembershipModel(
            circle_id = circle_id,
            user_id = circle_membership_data["user_id"],
            role = circle_membership_data["role"]
        )

        try:
            db.session.add(new_membership)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="There was an issue adding the member to the circle.")

        return {"message": "User is successfully added to the circle."}
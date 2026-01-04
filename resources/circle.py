from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required
)

from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import CircleModel, CircleMembershipModel, UserModel, GoalModel, CheckInModel
from sqlalchemy import func, desc

from schemas import CircleSchema, CircleMemberSchema, UserSchema, CircleAndUserSchema, CircleMemberRemoveSchema, CircleLeaderboardSchema

blp = Blueprint("circles", __name__, description="Operations on Circle")

@blp.route("/circles")
class CircleList(MethodView):
    @jwt_required()
    @blp.response(200, CircleSchema(many=True))
    def get(self):
        """Get all circles the current user is a member of"""
        current_user_id = int(get_jwt_identity())

        # Get all circles where user is a member
        memberships = CircleMembershipModel.query.filter_by(user_id=current_user_id).all()
        circles = [CircleModel.query.get(m.circle_id) for m in memberships]

        return circles

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
        return {
                "circle": circle,
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

    # @blp.arguments(CircleMemberSchema)
    # @blp.arguments(CircleAndUserSchema)
    @blp.arguments(CircleMemberSchema)
    @blp.response(200,CircleMemberRemoveSchema)
    def delete(self, circle_membership_data, circle_id):
        circle = CircleModel.query.get_or_404(circle_id)
        user = UserModel.query.get_or_404(circle_membership_data["user_id"])

        if user not in circle.users:
            abort(404, message="User is not in the circle.")

        circle.users.remove(user)

        try:
            db.session.add(circle)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occurred while removing the user from the circle.")

        return {"message": "User removed from the circle.", "user": user.id, "circle":circle.id}


@blp.route("/circle/<int:circle_id>/leaderboard")
class CircleLeaderboard(MethodView):
    @jwt_required()
    @blp.response(200, CircleLeaderboardSchema)
    def get(self, circle_id):
        """
        Get leaderboard for a circle showing member activity and progress.

        Returns stats for each member including:
        - Total check-ins count
        - Active goals count
        - Last check-in timestamp
        - Member since date

        Ordered by total check-ins (most active first).
        """
        current_user_id = int(get_jwt_identity())

        # Verify circle exists and user is a member
        circle = CircleModel.query.get_or_404(circle_id)

        # Check if user is a member of the circle
        membership = CircleMembershipModel.query.filter_by(
            circle_id=circle_id,
            user_id=current_user_id
        ).first()

        if not membership:
            abort(403, message="You must be a member of this circle to view the leaderboard")

        # Get all members of the circle
        members = CircleMembershipModel.query.filter_by(circle_id=circle_id).all()

        leaderboard_data = []

        for member in members:
            user = UserModel.query.get(member.user_id)

            # Count total check-ins for this user's goals in this circle
            total_check_ins = db.session.query(func.count(CheckInModel.id)).join(
                GoalModel
            ).filter(
                GoalModel.user_id == user.id,
                GoalModel.circle_id == circle_id
            ).scalar() or 0

            # Count active goals in this circle
            active_goals = GoalModel.query.filter_by(
                user_id=user.id,
                circle_id=circle_id,
                is_active=True
            ).count()

            # Get last check-in timestamp for this user's circle goals
            last_check_in = db.session.query(func.max(CheckInModel.created_at)).join(
                GoalModel
            ).filter(
                GoalModel.user_id == user.id,
                GoalModel.circle_id == circle_id
            ).scalar()

            leaderboard_data.append({
                "user_id": user.id,
                "username": user.username,
                "total_check_ins": total_check_ins,
                "active_goals": active_goals,
                "last_check_in": last_check_in,
                "member_since": member.joined_at,
                "role": member.role
            })

        # Sort by total check-ins (descending)
        leaderboard_data.sort(key=lambda x: x["total_check_ins"], reverse=True)

        return {
            "circle_id": circle.id,
            "circle_name": circle.name,
            "leaderboard": leaderboard_data
        }
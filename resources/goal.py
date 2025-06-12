from db import db
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from schemas import GoalSchema, GoalUpdateSchema

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from models import GoalModel


blp = Blueprint("goals", __name__, description="Operations on goals.")

@blp.route("/goals")
class GoalList(MethodView):
    @jwt_required()
    @blp.arguments(GoalSchema)
    @blp.response(201)
    def post(self, goal_data):
        current_user = get_jwt_identity()
        goal = GoalModel(
            **goal_data,
            user_id = current_user
        )

        try:
            db.session.add(goal)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="An error occurred while creating a goal")
            # return {"message": str(e)}

        return {"message": "Goal successfully created"}
    @jwt_required()
    @blp.response(200, GoalSchema(many=True))
    def get(self):
        current_user = get_jwt_identity()
        # goals = GoalModel.query.filter_by(created_by=current_user).all()
        user_goals = GoalModel.query.filter_by(user_id=current_user)

        return user_goals

@blp.route("/goal/<string:goal_id>")
class Goal(MethodView):
    @jwt_required()
    @blp.response(201, GoalSchema)
    def get(self, goal_id):
        goal = GoalModel.query.get_or_404(goal_id)

        return goal

    @jwt_required()
    @blp.arguments(GoalUpdateSchema)
    @blp.response(201)
    def put(self, goal_data, goal_id):
        goal = GoalModel.query.get_or_404(goal_id)
        current_user_id = get_jwt_identity()
        # return {"this": current_user_id}
        # return {"this": goal.user_id}
        if goal.user_id != int(current_user_id):
            abort(403, message="The user does cannot modify the goal")

        for field in goal_data:
            setattr(goal, field, goal_data[field])

        try:
            db.session.add(goal)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the goal")

        return {"message": "Goal successfully updated"}

    @jwt_required(fresh=True)
    @blp.response(204)
    def delete(self, goal_id):
        goal = GoalModel.query.get_or_404(goal_id)
        current_user = get_jwt_identity()

        if goal.user_id != int(current_user):
            abort(403, message="The user cannot delete the goal")

        try:
            db.session.delete(goal)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="There was an issue while deleting the goal")

        return {"message": "Goal successfully deleted"}
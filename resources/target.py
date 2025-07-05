from db import db
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView

from models import TargetModel, CheckInModel

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from schemas import TargetSchema, CheckInSchema, CheckInListSchema

blp = Blueprint("targets", __name__, description="Operations on targets")

@blp.route("/targets")
class TargetCreate(MethodView):
    @jwt_required()
    @blp.response(200)
    @blp.arguments(TargetSchema)
    def post(self, target_data):
        current_user_id = get_jwt_identity()
        target = TargetModel(**target_data, user_id=current_user_id)

        try:
            db.session.add(target)
            db.session.commit()
        except SQLAlchemyError as e:
            # abort(500, message="An error occurred while creating the target")
            abort(500, message=str(e))

        return {"message": "Target created successfully"}

@blp.route("/target/<int:target_id>")
class Target(MethodView):
    @jwt_required()
    @blp.response(201, TargetSchema)
    def get(self, target_id):
        current_user_id = get_jwt_identity()
        target = TargetModel.query.get_or_404(target_id)

        #TODO: Make friends be able to view
        if not target.user_id == int(current_user_id):
            abort(500, message="You do not have the permission to view the target")

        return target

    @jwt_required()
    # @blp.response(204)
    def delete(self, target_id):
        current_user_id = get_jwt_identity()
        target = TargetModel.query.get_or_404(target_id)

        if not target.user_id == int(current_user_id):
            abort(500, message="You do not have the permission to delete the target")

        try:
            db.session.delete(target)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the target")
        #Currently not returning the sucessful deletion message
        return {"message": f"target {target.title} successfully deleted"}, 204

@blp.route("/target/<int:target_id>/check-ins")
class TargetCheckInList(MethodView):
    @jwt_required()
    @blp.arguments(CheckInSchema)
    def post(self, check_in_data, target_id):
        current_user_id = get_jwt_identity()
        check_in = CheckInModel(**check_in_data, user_id=current_user_id,
                                target_id=target_id)

        try:
            db.session.add(check_in)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the check in")

        return {"message": "Check in successfully created"}

    @jwt_required()
    @blp.response(200, CheckInListSchema)
    def get(self, target_id):
        target = TargetModel.query.get_or_404(target_id)

        return({"check_ins":target.check_ins})


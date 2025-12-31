from db import db
from flask_smorest import Blueprint, abort
from flask.views import MethodView

from models import(
    CheckInModel,
    CommentModel,
    ReactModel
)
from schemas import(
    CheckInSchema,
    CheckInCommentSchema,
    CheckInCommentListSchema,
    ReactSchema
)

from flask_jwt_extended import(
    jwt_required,
    get_jwt_identity
)

from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("check_ins", __name__, description="Operations on Check-Ins")

@blp.route("/check-ins/<int:check_in_id>")
class CheckIn(MethodView):
    @jwt_required()
    @blp.response(201, CheckInSchema)
    def get(self, check_in_id):
        check_in = CheckInModel.query.get_or_404(check_in_id)
        return(check_in)

@blp.route("/check-ins/<int:check_in_id>/comments")
class CheckInCommentsList(MethodView):
    @jwt_required()
    @blp.arguments(CheckInCommentSchema)
    def post(self, check_in_comment_data, check_in_id):
        current_user_id = get_jwt_identity()

        # Validate check-in exists before creating comment
        check_in = CheckInModel.query.get_or_404(check_in_id)

        comment = CommentModel(user_id=current_user_id,
                               check_in_id=check_in_id,
                               **check_in_comment_data
                               )

        try:
            db.session.add(comment)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="An error occurred while creating the comment")
            # return (str(e))

        return {"message": "Successfully commented the comment"}, 200

    @jwt_required()
    @blp.response(201,CheckInCommentSchema(many=True))
    def get(self, check_in_id):
        check_in = CheckInModel.query.get_or_404(check_in_id)
        return(check_in.comments)

@blp.route("/check-ins/<int:check_in_id>/reactions")
class CheckInReactsList(MethodView):
    @jwt_required()
    @blp.arguments(ReactSchema)
    #Need to limit to one reaction per user for each check in
    def post(self, react_data, check_in_id):
        current_user_id = get_jwt_identity()
        react = ReactModel(user_id=current_user_id,
                           check_in_id=check_in_id,
                           **react_data)

        try:
            db.session.add(react)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the react")

        return {"message": "React successfully created"}, 201

    #this return is ugly, fix it.
    @blp.response(200, ReactSchema(many=True))
    def get(self, check_in_id):
        check_in = CheckInModel.query.get_or_404(check_in_id)

        return(check_in.reactions)
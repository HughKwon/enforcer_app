from db import db

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from models import CommentModel, ReactModel
from schemas import ReactSchema

from flask_jwt_extended import(
    get_jwt_identity,
    jwt_required
)

blp = Blueprint("comments", __name__, description="Operations on comments")

@blp.route("/comments/<int:comment_id>")
class Comment(MethodView):
    @jwt_required(fresh=True)
    def delete(self, comment_id):
        comment = CommentModel.query.get_or_404(comment_id)

        try:
            db.session.delete(comment)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the comment")

        return {"message": "Comment successfully deleted."}, 204

@blp.route("/comments/<int:comment_id>/reactions")
class CommentReactsList(MethodView):
    @jwt_required()
    @blp.arguments(ReactSchema)
    def post(self, react_data, comment_id):
        current_user_id = get_jwt_identity()
        # Validate comment exists before creating reaction
        comment = CommentModel.query.get_or_404(comment_id)

        reaction = ReactModel(
            comment_id=comment_id,
            user_id=current_user_id,
            **react_data
        )

        try:
            db.session.add(reaction)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the reaction")

        return {"message": "Reaction successfully created"}, 201

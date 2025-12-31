from db import db
from flask_smorest import Blueprint, abort
from flask.views import MethodView

from sqlalchemy.exc import SQLAlchemyError

from models import ReactModel
from schemas import ReactSchema

from flask_jwt_extended import(
    get_jwt_identity,
    jwt_required
)

blp = Blueprint("reactions", __name__, description="Operations on reactions")

@blp.route("/reactions/<int:reaction_id>")
class Reaction(MethodView):
    @jwt_required()
    @blp.arguments(ReactSchema)
    def put(self, reaction_data, reaction_id):
        current_user_id = get_jwt_identity()
        reaction = ReactModel.query.get_or_404(reaction_id)
        print(reaction.user_id)
        print(current_user_id)
        if reaction.user_id != int(current_user_id):
            abort(401, message="You have no permission to update this reaction.")

        for field in reaction_data:
            setattr(reaction, field, reaction_data[field])

        try:
            db.session.add(reaction)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occurred while updating the reaction.")

        return {"message": "The reaction was successfully updated"}, 200

    @jwt_required()
    def delete(self, reaction_id):
        current_user_id = get_jwt_identity()
        reaction = ReactModel.query.get_or_404(reaction_id)
        if reaction.user_id != int(current_user_id):
            abort(401, message="You have no permission to remove this reaction.")

        try:
            db.session.delete(reaction)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occurred while removing the reaction.")

        return {"message": "The reaction was successfully removed."}, 200



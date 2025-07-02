from flask_smorest import Blueprint, abort

from db import db
from sqlalchemy.exc import SQLAlchemyError

from flask.views import MethodView
from models import UserModel, FollowModel

from schemas import FollowersSchema, FollowingSchema

from flask_jwt_extended import(
    jwt_required,
    get_jwt_identity
)

blp = Blueprint("follows", __name__, description="Operations on follows")

@blp.route("/follow/<int:user_id>")
class FollowUser(MethodView):
    @jwt_required()
    @blp.response(201)
    def post(self, user_id):
        current_user = get_jwt_identity()
        following_user = UserModel.query.get_or_404(user_id)

        follow = FollowModel(follower_id=current_user,
                             following_id=following_user.id
                             )
        try:
            db.session.add(follow)
            db.session.commit()
        except SQLAlchemyError as e:
            # abort(500, message="An error occurred during applying the follow request.")
            abort(500, message=str(e))

        return {"message": "User followed successfully"}

    @jwt_required()
    @blp.response(201)
    def delete(self, user_id):
        current_user_id = get_jwt_identity()
        unfollow_user_id = UserModel.query.get_or_404(user_id)

        follow = FollowModel.query.filter_by(
            follower_id = current_user_id,
            following_id = user_id
        ).first()

        if not follow:
            abort(404, message="Follow relationship does not exist")
        try:
            db.session.delete(follow)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occurred while performing the unfollow request." )

        return {"message": "User unfollowed successfully"}



@blp.route("/followings")
class UserFollowings(MethodView):
    @jwt_required()
    @blp.response(200,FollowingSchema)
    def get(self):
        current_user_id = get_jwt_identity()
        # FollowModel.query.filter_by(current_user)
        current_user = UserModel.query.get_or_404(current_user_id)

        # return followings
        return {"followings": current_user.followings}

@blp.route("/followers")
class UserFollowers(MethodView):
    @jwt_required()
    @blp.response(200, FollowersSchema)
    def get(self):
        current_user_id = get_jwt_identity()
        current_user = UserModel.query.get_or_404(current_user_id)

        return {"followers": current_user.followers}

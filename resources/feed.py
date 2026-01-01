from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc, or_

from db import db
from models import CheckInModel, FollowModel, CircleMembershipModel
from schemas import FeedSchema

blp = Blueprint("feed", __name__, description="Operations on user feed/timeline")


@blp.route("/feed")
class Feed(MethodView):
    @jwt_required()
    @blp.response(200, FeedSchema)
    def get(self):
        """
        Get personalized feed for the current user.

        Returns check-ins from:
        1. Users the current user follows
        2. Users in circles the current user is part of
        3. Current user's own check-ins

        Results are ordered by most recent first.
        """
        current_user_id = int(get_jwt_identity())

        # Get IDs of users the current user follows
        following_ids_query = db.session.query(FollowModel.following_id).filter(
            FollowModel.follower_id == current_user_id
        )
        following_ids = [row[0] for row in following_ids_query.all()]

        # Get IDs of circles the current user is a member of
        circle_ids_query = db.session.query(CircleMembershipModel.circle_id).filter(
            CircleMembershipModel.user_id == current_user_id
        )
        circle_ids = [row[0] for row in circle_ids_query.all()]

        # Get IDs of all users in those circles (excluding current user to avoid duplicates)
        circle_member_ids = []
        if circle_ids:
            circle_members_query = db.session.query(CircleMembershipModel.user_id).filter(
                CircleMembershipModel.circle_id.in_(circle_ids),
                CircleMembershipModel.user_id != current_user_id
            ).distinct()
            circle_member_ids = [row[0] for row in circle_members_query.all()]

        # Combine all user IDs (followers + circle members + self)
        # Use set to remove duplicates, then convert to list
        feed_user_ids = list(set(following_ids + circle_member_ids + [current_user_id]))

        # If no users to show feed from, return empty feed
        if not feed_user_ids:
            return {"feed": []}

        # Get check-ins from all these users, ordered by most recent
        feed_check_ins = CheckInModel.query.filter(
            CheckInModel.user_id.in_(feed_user_ids)
        ).order_by(desc(CheckInModel.created_at)).limit(50).all()

        return {"feed": feed_check_ins}


@blp.route("/feed/following")
class FollowingFeed(MethodView):
    @jwt_required()
    @blp.response(200, FeedSchema)
    def get(self):
        """
        Get feed containing only check-ins from users the current user follows.

        This is a filtered view showing only activity from followed users.
        Results are ordered by most recent first.
        """
        current_user_id = int(get_jwt_identity())

        # Get IDs of users the current user follows
        following_ids_query = db.session.query(FollowModel.following_id).filter(
            FollowModel.follower_id == current_user_id
        )
        following_ids = [row[0] for row in following_ids_query.all()]

        # If not following anyone, return empty feed
        if not following_ids:
            return {"feed": []}

        # Get check-ins from followed users only
        feed_check_ins = CheckInModel.query.filter(
            CheckInModel.user_id.in_(following_ids)
        ).order_by(desc(CheckInModel.created_at)).limit(50).all()

        return {"feed": feed_check_ins}


@blp.route("/feed/circles")
class CirclesFeed(MethodView):
    @jwt_required()
    @blp.response(200, FeedSchema)
    def get(self):
        """
        Get feed containing only check-ins from users in the same circles.

        This is a filtered view showing only activity from circle members.
        Results are ordered by most recent first.
        """
        current_user_id = int(get_jwt_identity())

        # Get IDs of circles the current user is a member of
        circle_ids_query = db.session.query(CircleMembershipModel.circle_id).filter(
            CircleMembershipModel.user_id == current_user_id
        )
        circle_ids = [row[0] for row in circle_ids_query.all()]

        # If not in any circles, return empty feed
        if not circle_ids:
            return {"feed": []}

        # Get IDs of all users in those circles
        circle_members_query = db.session.query(CircleMembershipModel.user_id).filter(
            CircleMembershipModel.circle_id.in_(circle_ids)
        ).distinct()
        circle_member_ids = [row[0] for row in circle_members_query.all()]

        # If no members found, return empty feed
        if not circle_member_ids:
            return {"feed": []}

        # Get check-ins from circle members
        feed_check_ins = CheckInModel.query.filter(
            CheckInModel.user_id.in_(circle_member_ids)
        ).order_by(desc(CheckInModel.created_at)).limit(50).all()

        return {"feed": feed_check_ins}

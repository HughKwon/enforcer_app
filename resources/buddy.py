from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from db import db
from models import BuddyRequestModel, FollowModel, UserModel
from schemas import BuddyRequestSchema, BuddyRequestCreateSchema, BuddyListSchema

blp = Blueprint("buddy", __name__, description="Operations on accountability buddies")


@blp.route("/buddy/request/<int:user_id>")
class BuddyRequest(MethodView):
    @jwt_required()
    @blp.arguments(BuddyRequestCreateSchema)
    @blp.response(201)
    def post(self, request_data, user_id):
        """
        Send an accountability buddy request to another user.

        The request will be pending until the other user accepts or declines it.
        """
        current_user_id = int(get_jwt_identity())

        # Can't send buddy request to yourself
        if current_user_id == user_id:
            abort(400, message="You cannot send a buddy request to yourself")

        # Verify target user exists
        target_user = UserModel.query.get_or_404(user_id)

        # Check if they're already buddies
        existing_buddy = FollowModel.query.filter_by(
            follower_id=current_user_id,
            following_id=user_id,
            relationship_type=FollowModel.TYPE_BUDDY
        ).first()

        if existing_buddy:
            abort(400, message=f"You are already accountability buddies with {target_user.username}")

        # Check if there's already a pending request
        existing_request = BuddyRequestModel.query.filter_by(
            from_user_id=current_user_id,
            to_user_id=user_id,
            status=BuddyRequestModel.STATUS_PENDING
        ).first()

        if existing_request:
            abort(400, message="You already have a pending buddy request to this user")

        # Create buddy request
        buddy_request = BuddyRequestModel(
            from_user_id=current_user_id,
            to_user_id=user_id,
            message=request_data.get('message', '')
        )

        try:
            db.session.add(buddy_request)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the buddy request")

        return {"message": f"Buddy request sent to {target_user.username}"}


@blp.route("/buddy/requests/received")
class BuddyRequestsReceived(MethodView):
    @jwt_required()
    @blp.response(200, BuddyRequestSchema(many=True))
    def get(self):
        """
        Get all pending buddy requests received by the current user.
        """
        current_user_id = int(get_jwt_identity())

        requests = BuddyRequestModel.query.filter_by(
            to_user_id=current_user_id,
            status=BuddyRequestModel.STATUS_PENDING
        ).all()

        return requests


@blp.route("/buddy/requests/sent")
class BuddyRequestsSent(MethodView):
    @jwt_required()
    @blp.response(200, BuddyRequestSchema(many=True))
    def get(self):
        """
        Get all buddy requests sent by the current user.
        """
        current_user_id = int(get_jwt_identity())

        requests = BuddyRequestModel.query.filter_by(
            from_user_id=current_user_id
        ).all()

        return requests


@blp.route("/buddy/request/<int:request_id>/accept")
class BuddyRequestAccept(MethodView):
    @jwt_required()
    @blp.response(200)
    def post(self, request_id):
        """
        Accept a buddy request.

        This will create mutual buddy relationships (both users become buddies).
        If a follow relationship doesn't exist, it will be created.
        """
        current_user_id = int(get_jwt_identity())

        # Get the request
        buddy_request = BuddyRequestModel.query.get_or_404(request_id)

        # Verify the request is for the current user
        if buddy_request.to_user_id != current_user_id:
            abort(403, message="You can only accept buddy requests sent to you")

        # Verify request is still pending
        if buddy_request.status != BuddyRequestModel.STATUS_PENDING:
            abort(400, message="This buddy request has already been responded to")

        # Update request status
        buddy_request.status = BuddyRequestModel.STATUS_ACCEPTED
        buddy_request.responded_at = datetime.utcnow()

        # Create or update mutual buddy relationships
        # From requester to receiver
        follow1 = FollowModel.query.filter_by(
            follower_id=buddy_request.from_user_id,
            following_id=current_user_id
        ).first()

        if follow1:
            follow1.relationship_type = FollowModel.TYPE_BUDDY
        else:
            follow1 = FollowModel(
                follower_id=buddy_request.from_user_id,
                following_id=current_user_id,
                relationship_type=FollowModel.TYPE_BUDDY
            )
            db.session.add(follow1)

        # From receiver to requester
        follow2 = FollowModel.query.filter_by(
            follower_id=current_user_id,
            following_id=buddy_request.from_user_id
        ).first()

        if follow2:
            follow2.relationship_type = FollowModel.TYPE_BUDDY
        else:
            follow2 = FollowModel(
                follower_id=current_user_id,
                following_id=buddy_request.from_user_id,
                relationship_type=FollowModel.TYPE_BUDDY
            )
            db.session.add(follow2)

        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while accepting the buddy request")

        from_user = UserModel.query.get(buddy_request.from_user_id)
        return {"message": f"You are now accountability buddies with {from_user.username}"}


@blp.route("/buddy/request/<int:request_id>/decline")
class BuddyRequestDecline(MethodView):
    @jwt_required()
    @blp.response(200)
    def post(self, request_id):
        """
        Decline a buddy request.
        """
        current_user_id = int(get_jwt_identity())

        # Get the request
        buddy_request = BuddyRequestModel.query.get_or_404(request_id)

        # Verify the request is for the current user
        if buddy_request.to_user_id != current_user_id:
            abort(403, message="You can only decline buddy requests sent to you")

        # Verify request is still pending
        if buddy_request.status != BuddyRequestModel.STATUS_PENDING:
            abort(400, message="This buddy request has already been responded to")

        # Update request status
        buddy_request.status = BuddyRequestModel.STATUS_DECLINED
        buddy_request.responded_at = datetime.utcnow()

        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while declining the buddy request")

        return {"message": "Buddy request declined"}


@blp.route("/buddy/list")
class BuddyList(MethodView):
    @jwt_required()
    @blp.response(200, BuddyListSchema)
    def get(self):
        """
        Get all accountability buddies for the current user.
        """
        current_user_id = int(get_jwt_identity())

        # Get all buddy relationships
        buddy_relationships = FollowModel.query.filter_by(
            follower_id=current_user_id,
            relationship_type=FollowModel.TYPE_BUDDY
        ).all()

        buddies = []
        for rel in buddy_relationships:
            buddy = UserModel.query.get(rel.following_id)
            if buddy:
                buddies.append({
                    "user_id": buddy.id,
                    "username": buddy.username,
                    "email": buddy.email,
                    "buddies_since": rel.created_at
                })

        return {"buddies": buddies}


@blp.route("/buddy/<int:user_id>/remove")
class BuddyRemove(MethodView):
    @jwt_required()
    @blp.response(200)
    def delete(self, user_id):
        """
        Remove a user as an accountability buddy.

        This downgrades the buddy relationship back to a regular follow
        (or removes it entirely if no follow relationship exists).
        """
        current_user_id = int(get_jwt_identity())

        # Get the buddy relationships
        follow1 = FollowModel.query.filter_by(
            follower_id=current_user_id,
            following_id=user_id,
            relationship_type=FollowModel.TYPE_BUDDY
        ).first()

        follow2 = FollowModel.query.filter_by(
            follower_id=user_id,
            following_id=current_user_id,
            relationship_type=FollowModel.TYPE_BUDDY
        ).first()

        if not follow1:
            abort(404, message="You are not accountability buddies with this user")

        # Downgrade to regular follow or remove
        follow1.relationship_type = FollowModel.TYPE_FOLLOW
        if follow2:
            follow2.relationship_type = FollowModel.TYPE_FOLLOW

        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while removing the buddy relationship")

        user = UserModel.query.get(user_id)
        return {"message": f"Removed {user.username} as accountability buddy"}

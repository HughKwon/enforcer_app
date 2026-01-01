import pytest
from flask_jwt_extended import create_access_token
from models import (
    UserModel, CheckInModel, GoalModel, FollowModel,
    CircleModel, CircleMembershipModel
)
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta


class TestFeed:
    def test_get_feed_empty_when_no_activity(self, client, test_user, auth_token):
        """Test that feed returns empty when user has no activity to show."""
        response = client.get(
            "/feed",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "feed" in response.json
        # Should only contain user's own check-ins (none exist yet)
        assert len(response.json["feed"]) == 0

    def test_get_feed_shows_own_check_ins(self, client, test_user, test_goal, auth_token, db):
        """Test that feed shows user's own check-ins."""
        # Create a check-in for the test user
        check_in = CheckInModel(
            user_id=test_user.id,
            goal_id=test_goal.id,
            content="My first check-in"
        )
        db.session.add(check_in)
        db.session.commit()

        response = client.get(
            "/feed",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert len(response.json["feed"]) == 1
        assert response.json["feed"][0]["content"] == "My first check-in"

    def test_get_feed_shows_followed_users_check_ins(self, client, app, test_user, test_goal, db):
        """Test that feed shows check-ins from followed users."""
        # Create another user
        other_user = UserModel(
            username="otheruser",
            email="other@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(other_user)
        db.session.commit()

        # Create a goal for other user
        other_goal = GoalModel(
            title="Other Goal",
            description="Another goal",
            goal_type="daily",
            user_id=other_user.id,
            is_active=True
        )
        db.session.add(other_goal)
        db.session.commit()

        # Create a check-in for other user
        other_check_in = CheckInModel(
            user_id=other_user.id,
            goal_id=other_goal.id,
            content="Check-in from followed user"
        )
        db.session.add(other_check_in)
        db.session.commit()

        # Create follow relationship (test_user follows other_user)
        follow = FollowModel(
            follower_id=test_user.id,
            following_id=other_user.id
        )
        db.session.add(follow)
        db.session.commit()

        # Generate token for test_user
        with app.app_context():
            token = create_access_token(identity=str(test_user.id), fresh=False)

        response = client.get(
            "/feed",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert len(response.json["feed"]) == 1
        assert response.json["feed"][0]["content"] == "Check-in from followed user"

    def test_get_feed_shows_circle_members_check_ins(self, client, app, test_user, db):
        """Test that feed shows check-ins from circle members."""
        # Create a circle
        circle = CircleModel(
            name="Test Circle",
            description="A test circle",
            created_by_id=test_user.id
        )
        db.session.add(circle)
        db.session.commit()

        # Create another user
        circle_member = UserModel(
            username="circlemember",
            email="member@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(circle_member)
        db.session.commit()

        # Add both users to the circle
        membership1 = CircleMembershipModel(
            circle_id=circle.id,
            user_id=test_user.id,
            role="admin"
        )
        membership2 = CircleMembershipModel(
            circle_id=circle.id,
            user_id=circle_member.id,
            role="member"
        )
        db.session.add(membership1)
        db.session.add(membership2)
        db.session.commit()

        # Create a goal for circle member
        member_goal = GoalModel(
            title="Member Goal",
            description="Circle member's goal",
            goal_type="daily",
            user_id=circle_member.id,
            is_active=True
        )
        db.session.add(member_goal)
        db.session.commit()

        # Create a check-in for circle member
        member_check_in = CheckInModel(
            user_id=circle_member.id,
            goal_id=member_goal.id,
            content="Check-in from circle member"
        )
        db.session.add(member_check_in)
        db.session.commit()

        # Generate token for test_user
        with app.app_context():
            token = create_access_token(identity=str(test_user.id), fresh=False)

        response = client.get(
            "/feed",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert len(response.json["feed"]) == 1
        assert response.json["feed"][0]["content"] == "Check-in from circle member"

    def test_get_feed_combines_all_sources(self, client, app, test_user, test_goal, db):
        """Test that feed combines check-ins from all sources (self, followed, circles)."""
        # Create own check-in
        own_check_in = CheckInModel(
            user_id=test_user.id,
            goal_id=test_goal.id,
            content="My own check-in"
        )
        db.session.add(own_check_in)

        # Create followed user and their check-in
        followed_user = UserModel(
            username="followed",
            email="followed@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(followed_user)
        db.session.commit()

        followed_goal = GoalModel(
            title="Followed Goal",
            description="Goal",
            goal_type="daily",
            user_id=followed_user.id,
            is_active=True
        )
        db.session.add(followed_goal)
        db.session.commit()

        followed_check_in = CheckInModel(
            user_id=followed_user.id,
            goal_id=followed_goal.id,
            content="Followed user check-in"
        )
        db.session.add(followed_check_in)

        # Create follow relationship
        follow = FollowModel(
            follower_id=test_user.id,
            following_id=followed_user.id
        )
        db.session.add(follow)

        # Create circle with member
        circle = CircleModel(
            name="Circle",
            description="Test",
            created_by_id=test_user.id
        )
        db.session.add(circle)
        db.session.commit()

        circle_member = UserModel(
            username="circlemember",
            email="circlemember@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(circle_member)
        db.session.commit()

        membership1 = CircleMembershipModel(
            circle_id=circle.id,
            user_id=test_user.id,
            role="admin"
        )
        membership2 = CircleMembershipModel(
            circle_id=circle.id,
            user_id=circle_member.id,
            role="member"
        )
        db.session.add(membership1)
        db.session.add(membership2)
        db.session.commit()

        member_goal = GoalModel(
            title="Member Goal",
            description="Goal",
            goal_type="daily",
            user_id=circle_member.id,
            is_active=True
        )
        db.session.add(member_goal)
        db.session.commit()

        circle_check_in = CheckInModel(
            user_id=circle_member.id,
            goal_id=member_goal.id,
            content="Circle member check-in"
        )
        db.session.add(circle_check_in)
        db.session.commit()

        # Generate token
        with app.app_context():
            token = create_access_token(identity=str(test_user.id), fresh=False)

        response = client.get(
            "/feed",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert len(response.json["feed"]) == 3
        contents = [item["content"] for item in response.json["feed"]]
        assert "My own check-in" in contents
        assert "Followed user check-in" in contents
        assert "Circle member check-in" in contents

    def test_get_feed_orders_by_most_recent(self, client, app, test_user, test_goal, db):
        """Test that feed orders check-ins by most recent first."""
        # Create check-ins with different timestamps
        old_check_in = CheckInModel(
            user_id=test_user.id,
            goal_id=test_goal.id,
            content="Old check-in",
            created_at=datetime.utcnow() - timedelta(days=2)
        )
        recent_check_in = CheckInModel(
            user_id=test_user.id,
            goal_id=test_goal.id,
            content="Recent check-in",
            created_at=datetime.utcnow()
        )
        db.session.add(old_check_in)
        db.session.add(recent_check_in)
        db.session.commit()

        with app.app_context():
            token = create_access_token(identity=str(test_user.id), fresh=False)

        response = client.get(
            "/feed",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert len(response.json["feed"]) == 2
        # Most recent should be first
        assert response.json["feed"][0]["content"] == "Recent check-in"
        assert response.json["feed"][1]["content"] == "Old check-in"

    def test_get_feed_requires_authentication(self, client):
        """Test that feed endpoint requires authentication."""
        response = client.get("/feed")
        assert response.status_code == 401

    def test_get_feed_limits_to_50_items(self, client, app, test_user, test_goal, db):
        """Test that feed limits results to 50 items."""
        # Create 60 check-ins
        for i in range(60):
            check_in = CheckInModel(
                user_id=test_user.id,
                goal_id=test_goal.id,
                content=f"Check-in {i}",
                created_at=datetime.utcnow() - timedelta(hours=i)
            )
            db.session.add(check_in)
        db.session.commit()

        with app.app_context():
            token = create_access_token(identity=str(test_user.id), fresh=False)

        response = client.get(
            "/feed",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        # Should only return 50 most recent
        assert len(response.json["feed"]) == 50


class TestFollowingFeed:
    def test_get_following_feed_shows_only_followed_users(self, client, app, test_user, db):
        """Test that following feed shows only check-ins from followed users."""
        # Create followed user
        followed_user = UserModel(
            username="followed",
            email="followed@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(followed_user)
        db.session.commit()

        followed_goal = GoalModel(
            title="Goal",
            description="Goal",
            goal_type="daily",
            user_id=followed_user.id,
            is_active=True
        )
        db.session.add(followed_goal)
        db.session.commit()

        followed_check_in = CheckInModel(
            user_id=followed_user.id,
            goal_id=followed_goal.id,
            content="Followed check-in"
        )
        db.session.add(followed_check_in)

        # Create non-followed user
        other_user = UserModel(
            username="other",
            email="other@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(other_user)
        db.session.commit()

        other_goal = GoalModel(
            title="Other Goal",
            description="Goal",
            goal_type="daily",
            user_id=other_user.id,
            is_active=True
        )
        db.session.add(other_goal)
        db.session.commit()

        other_check_in = CheckInModel(
            user_id=other_user.id,
            goal_id=other_goal.id,
            content="Other check-in"
        )
        db.session.add(other_check_in)

        # Only follow first user
        follow = FollowModel(
            follower_id=test_user.id,
            following_id=followed_user.id
        )
        db.session.add(follow)
        db.session.commit()

        with app.app_context():
            token = create_access_token(identity=str(test_user.id), fresh=False)

        response = client.get(
            "/feed/following",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert len(response.json["feed"]) == 1
        assert response.json["feed"][0]["content"] == "Followed check-in"

    def test_get_following_feed_empty_when_not_following_anyone(self, client, app, test_user):
        """Test that following feed is empty when user follows no one."""
        with app.app_context():
            token = create_access_token(identity=str(test_user.id), fresh=False)

        response = client.get(
            "/feed/following",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert len(response.json["feed"]) == 0

    def test_get_following_feed_requires_authentication(self, client):
        """Test that following feed requires authentication."""
        response = client.get("/feed/following")
        assert response.status_code == 401


class TestCirclesFeed:
    def test_get_circles_feed_shows_only_circle_members(self, client, app, test_user, db):
        """Test that circles feed shows only check-ins from circle members."""
        # Create circle
        circle = CircleModel(
            name="Circle",
            description="Test",
            created_by_id=test_user.id
        )
        db.session.add(circle)
        db.session.commit()

        # Create circle member
        circle_member = UserModel(
            username="member",
            email="member@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(circle_member)
        db.session.commit()

        membership1 = CircleMembershipModel(
            circle_id=circle.id,
            user_id=test_user.id,
            role="admin"
        )
        membership2 = CircleMembershipModel(
            circle_id=circle.id,
            user_id=circle_member.id,
            role="member"
        )
        db.session.add(membership1)
        db.session.add(membership2)
        db.session.commit()

        member_goal = GoalModel(
            title="Goal",
            description="Goal",
            goal_type="daily",
            user_id=circle_member.id,
            is_active=True
        )
        db.session.add(member_goal)
        db.session.commit()

        member_check_in = CheckInModel(
            user_id=circle_member.id,
            goal_id=member_goal.id,
            content="Circle check-in"
        )
        db.session.add(member_check_in)

        # Create non-circle user
        other_user = UserModel(
            username="other",
            email="other@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(other_user)
        db.session.commit()

        other_goal = GoalModel(
            title="Other Goal",
            description="Goal",
            goal_type="daily",
            user_id=other_user.id,
            is_active=True
        )
        db.session.add(other_goal)
        db.session.commit()

        other_check_in = CheckInModel(
            user_id=other_user.id,
            goal_id=other_goal.id,
            content="Non-circle check-in"
        )
        db.session.add(other_check_in)
        db.session.commit()

        with app.app_context():
            token = create_access_token(identity=str(test_user.id), fresh=False)

        response = client.get(
            "/feed/circles",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert len(response.json["feed"]) == 1
        assert response.json["feed"][0]["content"] == "Circle check-in"

    def test_get_circles_feed_empty_when_not_in_circles(self, client, app, test_user):
        """Test that circles feed is empty when user is not in any circles."""
        with app.app_context():
            token = create_access_token(identity=str(test_user.id), fresh=False)

        response = client.get(
            "/feed/circles",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert len(response.json["feed"]) == 0

    def test_get_circles_feed_includes_own_check_ins_if_in_circle(self, client, app, test_user, db):
        """Test that circles feed includes user's own check-ins if they're in the circle."""
        # Create circle
        circle = CircleModel(
            name="Circle",
            description="Test",
            created_by_id=test_user.id
        )
        db.session.add(circle)
        db.session.commit()

        # Add user to circle
        membership = CircleMembershipModel(
            circle_id=circle.id,
            user_id=test_user.id,
            role="admin"
        )
        db.session.add(membership)
        db.session.commit()

        # Create goal and check-in for test user
        goal = GoalModel(
            title="Goal",
            description="Goal",
            goal_type="daily",
            user_id=test_user.id,
            is_active=True
        )
        db.session.add(goal)
        db.session.commit()

        check_in = CheckInModel(
            user_id=test_user.id,
            goal_id=goal.id,
            content="My check-in"
        )
        db.session.add(check_in)
        db.session.commit()

        with app.app_context():
            token = create_access_token(identity=str(test_user.id), fresh=False)

        response = client.get(
            "/feed/circles",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert len(response.json["feed"]) == 1
        assert response.json["feed"][0]["content"] == "My check-in"

    def test_get_circles_feed_requires_authentication(self, client):
        """Test that circles feed requires authentication."""
        response = client.get("/feed/circles")
        assert response.status_code == 401

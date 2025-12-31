import pytest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from models import UserModel, FollowModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256


@pytest.fixture(scope="function")
def second_user(db):
    """Create a second test user to follow."""
    user = UserModel(
        username="seconduser",
        email="second@example.com",
        password_hash=pbkdf2_sha256.hash("password"),
        is_staff=False
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope="function")
def third_user(db):
    """Create a third test user."""
    user = UserModel(
        username="thirduser",
        email="third@example.com",
        password_hash=pbkdf2_sha256.hash("password"),
        is_staff=False
    )
    db.session.add(user)
    db.session.commit()
    return user


class TestFollowUser:
    def test_post_follow_user_successfully(self, client, auth_token, second_user):
        """Test successfully following a user."""
        response = client.post(
            f"/follow/{second_user.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["message"] == "User followed successfully"

    def test_post_follow_user_not_found(self, client, auth_token):
        """Test following a non-existent user."""
        response = client.post(
            "/follow/9999",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_post_follow_user_without_auth(self, client, second_user):
        """Test following a user without authentication."""
        response = client.post(f"/follow/{second_user.id}")

        assert response.status_code == 401

    def test_post_follow_user_database_error(self, client, auth_token, second_user):
        """Test following a user with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.post(
                f"/follow/{second_user.id}",
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "Database error" in response.json["message"]

    def test_post_follow_user_already_following(self, client, auth_token, second_user, test_user, db):
        """Test following a user that is already being followed."""
        # Create existing follow relationship
        follow = FollowModel(
            follower_id=test_user.id,
            following_id=second_user.id
        )
        db.session.add(follow)
        db.session.commit()

        # Try to follow again
        response = client.post(
            f"/follow/{second_user.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # This will fail due to unique constraint
        assert response.status_code == 500

    def test_delete_unfollow_user_successfully(self, client, auth_token, second_user, test_user, db):
        """Test successfully unfollowing a user."""
        # Create follow relationship first
        follow = FollowModel(
            follower_id=test_user.id,
            following_id=second_user.id
        )
        db.session.add(follow)
        db.session.commit()

        # Unfollow
        response = client.delete(
            f"/follow/{second_user.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["message"] == "User unfollowed successfully"

    def test_delete_unfollow_user_not_following(self, client, auth_token, second_user):
        """Test unfollowing a user that is not being followed."""
        response = client.delete(
            f"/follow/{second_user.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404
        assert "does not exist" in response.json["message"]

    def test_delete_unfollow_user_not_found(self, client, auth_token):
        """Test unfollowing a non-existent user."""
        response = client.delete(
            "/follow/9999",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_delete_unfollow_user_database_error(self, client, auth_token, second_user, test_user, db):
        """Test unfollowing a user with database error."""
        # Create follow relationship
        follow = FollowModel(
            follower_id=test_user.id,
            following_id=second_user.id
        )
        db.session.add(follow)
        db.session.commit()

        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.delete(
                f"/follow/{second_user.id}",
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "error has occurred while performing the unfollow request" in response.json["message"]


class TestUserFollowings:
    def test_get_followings_successfully(self, client, auth_token, second_user, third_user, test_user, db):
        """Test retrieving list of users the current user is following."""
        # Create follow relationships
        follow1 = FollowModel(follower_id=test_user.id, following_id=second_user.id)
        follow2 = FollowModel(follower_id=test_user.id, following_id=third_user.id)
        db.session.add(follow1)
        db.session.add(follow2)
        db.session.commit()

        response = client.get(
            "/followings",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "followings" in response.json
        assert isinstance(response.json["followings"], list)
        assert len(response.json["followings"]) == 2

    def test_get_followings_empty_list(self, client, auth_token):
        """Test retrieving followings when user follows nobody."""
        response = client.get(
            "/followings",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "followings" in response.json
        assert isinstance(response.json["followings"], list)
        assert len(response.json["followings"]) == 0

    def test_get_followings_without_auth(self, client):
        """Test retrieving followings without authentication."""
        response = client.get("/followings")

        assert response.status_code == 401


class TestUserFollowers:
    def test_get_followers_successfully(self, client, auth_token, second_user, third_user, test_user, db):
        """Test retrieving list of users following the current user."""
        # Create follow relationships (other users following test_user)
        follow1 = FollowModel(follower_id=second_user.id, following_id=test_user.id)
        follow2 = FollowModel(follower_id=third_user.id, following_id=test_user.id)
        db.session.add(follow1)
        db.session.add(follow2)
        db.session.commit()

        response = client.get(
            "/followers",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "followers" in response.json
        assert isinstance(response.json["followers"], list)
        assert len(response.json["followers"]) == 2

    def test_get_followers_empty_list(self, client, auth_token):
        """Test retrieving followers when user has no followers."""
        response = client.get(
            "/followers",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "followers" in response.json
        assert isinstance(response.json["followers"], list)
        assert len(response.json["followers"]) == 0

    def test_get_followers_without_auth(self, client):
        """Test retrieving followers without authentication."""
        response = client.get("/followers")

        assert response.status_code == 401

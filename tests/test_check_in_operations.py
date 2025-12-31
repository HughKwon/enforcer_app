import pytest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from models import CheckInModel, CommentModel, ReactModel
from db import db
from sqlalchemy.exc import SQLAlchemyError


@pytest.fixture(scope="function")
def test_check_in(db, test_goal, test_user):
    """Create a test check-in."""
    check_in = CheckInModel(
        content="Test check-in content",
        goal_id=test_goal.id,
        user_id=test_user.id
    )
    db.session.add(check_in)
    db.session.commit()
    return check_in


class TestCheckIn:
    def test_get_check_in_successfully(self, client, test_check_in, auth_token):
        """Test retrieving a specific check-in by ID."""
        response = client.get(
            f"/check-ins/{test_check_in.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["content"] == test_check_in.content
        assert response.json["id"] == test_check_in.id

    def test_get_check_in_not_found(self, client, auth_token):
        """Test retrieving a non-existent check-in."""
        response = client.get(
            "/check-ins/9999",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_get_check_in_without_auth(self, client, test_check_in):
        """Test retrieving a check-in without authentication."""
        response = client.get(f"/check-ins/{test_check_in.id}")

        assert response.status_code == 401


class TestCheckInCommentsList:
    def test_post_create_comment_successfully(self, client, test_check_in, auth_token):
        """Test successfully creating a comment on a check-in."""
        response = client.post(
            f"/check-ins/{test_check_in.id}/comments",
            json={"content": "Great progress!"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "Successfully commented the comment"

    def test_post_create_comment_without_auth(self, client, test_check_in):
        """Test creating a comment without authentication."""
        response = client.post(
            f"/check-ins/{test_check_in.id}/comments",
            json={"content": "Great progress!"}
        )

        assert response.status_code == 401

    def test_post_create_comment_check_in_not_found(self, client, auth_token):
        """Test creating a comment on non-existent check-in."""
        response = client.post(
            "/check-ins/9999/comments",
            json={"content": "Great progress!"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # Should fail gracefully
        assert response.status_code in [404, 500]

    def test_post_create_comment_database_error(self, client, test_check_in, auth_token):
        """Test creating a comment with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.post(
                f"/check-ins/{test_check_in.id}/comments",
                json={"content": "Great progress!"},
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "error occurred while creating the comment" in response.json["message"]

    def test_get_check_in_comments_successfully(self, client, test_check_in, auth_token, db, test_user):
        """Test retrieving all comments for a check-in."""
        # Create a comment
        comment = CommentModel(
            content="Test comment",
            check_in_id=test_check_in.id,
            user_id=test_user.id
        )
        db.session.add(comment)
        db.session.commit()

        response = client.get(
            f"/check-ins/{test_check_in.id}/comments",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert isinstance(response.json, list)
        assert len(response.json) >= 1

    def test_get_check_in_comments_empty_list(self, client, test_check_in, auth_token):
        """Test retrieving comments when check-in has no comments."""
        response = client.get(
            f"/check-ins/{test_check_in.id}/comments",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert isinstance(response.json, list)

    def test_get_check_in_comments_not_found(self, client, auth_token):
        """Test retrieving comments for non-existent check-in."""
        response = client.get(
            "/check-ins/9999/comments",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404


class TestCheckInReactsList:
    def test_post_create_reaction_successfully(self, client, test_check_in, auth_token):
        """Test successfully creating a reaction on a check-in."""
        response = client.post(
            f"/check-ins/{test_check_in.id}/reactions",
            json={"react_type": "like"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["message"] == "React successfully created"

    def test_post_create_reaction_without_react_type(self, client, test_check_in, auth_token):
        """Test creating a reaction without specifying type."""
        response = client.post(
            f"/check-ins/{test_check_in.id}/reactions",
            json={},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # Should still succeed as react_type is optional
        assert response.status_code == 201
        assert response.json["message"] == "React successfully created"

    def test_post_create_reaction_without_auth(self, client, test_check_in):
        """Test creating a reaction without authentication."""
        response = client.post(
            f"/check-ins/{test_check_in.id}/reactions",
            json={"react_type": "like"}
        )

        assert response.status_code == 401

    def test_post_create_reaction_database_error(self, client, test_check_in, auth_token):
        """Test creating a reaction with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.post(
                f"/check-ins/{test_check_in.id}/reactions",
                json={"react_type": "like"},
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "error occurred while creating the react" in response.json["message"]

    def test_get_check_in_reactions_successfully(self, client, test_check_in, auth_token, db, test_user):
        """Test retrieving all reactions for a check-in."""
        # Create a reaction
        reaction = ReactModel(
            react_type="like",
            check_in_id=test_check_in.id,
            user_id=test_user.id
        )
        db.session.add(reaction)
        db.session.commit()

        response = client.get(
            f"/check-ins/{test_check_in.id}/reactions",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) >= 1

    def test_get_check_in_reactions_empty_list(self, client, test_check_in, auth_token):
        """Test retrieving reactions when check-in has no reactions."""
        response = client.get(
            f"/check-ins/{test_check_in.id}/reactions",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_get_check_in_reactions_not_found(self, client, auth_token):
        """Test retrieving reactions for non-existent check-in."""
        response = client.get(
            "/check-ins/9999/reactions",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

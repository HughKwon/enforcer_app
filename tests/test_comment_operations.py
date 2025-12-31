import pytest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from models import CommentModel, CheckInModel, UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256


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


@pytest.fixture(scope="function")
def test_comment(db, test_check_in, test_user):
    """Create a test comment."""
    comment = CommentModel(
        content="Test comment content",
        check_in_id=test_check_in.id,
        user_id=test_user.id
    )
    db.session.add(comment)
    db.session.commit()
    return comment


class TestComment:
    def test_delete_comment_successfully(self, client, test_comment, app, test_user):
        """Test successfully deleting a comment."""
        with app.app_context():
            fresh_token = create_access_token(identity=str(test_user.id), fresh=True)

        response = client.delete(
            f"/comments/{test_comment.id}",
            headers={"Authorization": f"Bearer {fresh_token}"}
        )

        assert response.status_code == 204
        # 204 No Content responses don't have a body, so check with get_json()
        if response.data:
            assert response.json["message"] == "Comment successfully deleted."

    def test_delete_comment_not_found(self, client, app, test_user):
        """Test deleting a non-existent comment."""
        with app.app_context():
            fresh_token = create_access_token(identity=str(test_user.id), fresh=True)

        response = client.delete(
            "/comments/9999",
            headers={"Authorization": f"Bearer {fresh_token}"}
        )

        assert response.status_code == 404

    def test_delete_comment_requires_fresh_token(self, client, test_comment, auth_token):
        """Test that deleting a comment requires a fresh token."""
        response = client.delete(
            f"/comments/{test_comment.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # Non-fresh token should be rejected
        assert response.status_code in [401, 422]

    def test_delete_comment_without_auth(self, client, test_comment):
        """Test deleting a comment without authentication."""
        response = client.delete(f"/comments/{test_comment.id}")

        assert response.status_code == 401

    def test_delete_comment_database_error(self, client, test_comment, app, test_user):
        """Test deleting a comment with database error."""
        with app.app_context():
            fresh_token = create_access_token(identity=str(test_user.id), fresh=True)

        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.delete(
                f"/comments/{test_comment.id}",
                headers={"Authorization": f"Bearer {fresh_token}"}
            )

            assert response.status_code == 500
            assert "error occurred while deleting the comment" in response.json["message"]


class TestCommentReactsList:
    def test_post_create_reaction_on_comment(self, client, test_comment, auth_token):
        """Test creating a reaction on a comment."""
        response = client.post(
            f"/comments/{test_comment.id}/reactions",
            json={"react_type": "like"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["message"] == "Reaction successfully created"

    def test_post_create_reaction_comment_not_found(self, client, auth_token):
        """Test creating a reaction on non-existent comment."""
        response = client.post(
            "/comments/9999/reactions",
            json={"react_type": "like"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_post_create_reaction_without_auth(self, client, test_comment):
        """Test creating a reaction without authentication."""
        response = client.post(f"/comments/{test_comment.id}/reactions")

        assert response.status_code == 401

import pytest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from models import ReactModel, CheckInModel, CommentModel, UserModel
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


@pytest.fixture(scope="function")
def test_reaction_on_check_in(db, test_check_in, test_user):
    """Create a test reaction on a check-in."""
    reaction = ReactModel(
        react_type="like",
        check_in_id=test_check_in.id,
        user_id=test_user.id
    )
    db.session.add(reaction)
    db.session.commit()
    return reaction


@pytest.fixture(scope="function")
def test_reaction_on_comment(db, test_comment, test_user):
    """Create a test reaction on a comment."""
    reaction = ReactModel(
        react_type="heart",
        comment_id=test_comment.id,
        user_id=test_user.id
    )
    db.session.add(reaction)
    db.session.commit()
    return reaction


class TestReaction:
    def test_put_update_reaction_successfully(self, client, test_reaction_on_check_in, auth_token):
        """Test successfully updating a reaction."""
        response = client.put(
            f"/reactions/{test_reaction_on_check_in.id}",
            json={"react_type": "love"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "The reaction was successfully updated"

    def test_put_update_reaction_unauthorized(self, client, test_reaction_on_check_in, app, db):
        """Test updating a reaction by a different user (unauthorized)."""
        # Create another user
        other_user = UserModel(
            username="otheruser",
            email="other@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(other_user)
        db.session.commit()

        with app.app_context():
            other_token = create_access_token(identity=str(other_user.id))

        response = client.put(
            f"/reactions/{test_reaction_on_check_in.id}",
            json={"react_type": "love"},
            headers={"Authorization": f"Bearer {other_token}"}
        )

        assert response.status_code == 401
        assert "no permission to update this reaction" in response.json["message"]

    def test_put_update_reaction_not_found(self, client, auth_token):
        """Test updating a non-existent reaction."""
        response = client.put(
            "/reactions/9999",
            json={"react_type": "love"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_put_update_reaction_database_error(self, client, test_reaction_on_check_in, auth_token):
        """Test updating a reaction with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.put(
                f"/reactions/{test_reaction_on_check_in.id}",
                json={"react_type": "love"},
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "error has occurred while updating the reaction" in response.json["message"]

    def test_put_update_reaction_without_auth(self, client, test_reaction_on_check_in):
        """Test updating a reaction without authentication."""
        response = client.put(
            f"/reactions/{test_reaction_on_check_in.id}",
            json={"react_type": "love"}
        )

        assert response.status_code == 401

    def test_delete_reaction_successfully(self, client, test_reaction_on_check_in, auth_token):
        """Test successfully deleting a reaction."""
        response = client.delete(
            f"/reactions/{test_reaction_on_check_in.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "The reaction was successfully removed."

    def test_delete_reaction_unauthorized(self, client, test_reaction_on_check_in, app, db):
        """Test deleting a reaction by a different user (unauthorized)."""
        # Create another user
        other_user = UserModel(
            username="otheruser",
            email="other@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(other_user)
        db.session.commit()

        with app.app_context():
            other_token = create_access_token(identity=str(other_user.id))

        response = client.delete(
            f"/reactions/{test_reaction_on_check_in.id}",
            headers={"Authorization": f"Bearer {other_token}"}
        )

        assert response.status_code == 401
        assert "no permission to remove this reaction" in response.json["message"]

    def test_delete_reaction_not_found(self, client, auth_token):
        """Test deleting a non-existent reaction."""
        response = client.delete(
            "/reactions/9999",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_delete_reaction_database_error(self, client, test_reaction_on_check_in, auth_token):
        """Test deleting a reaction with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.delete(
                f"/reactions/{test_reaction_on_check_in.id}",
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "error has occurred while removing the reaction" in response.json["message"]

    def test_delete_reaction_without_auth(self, client, test_reaction_on_check_in):
        """Test deleting a reaction without authentication."""
        response = client.delete(f"/reactions/{test_reaction_on_check_in.id}")

        assert response.status_code == 401

    def test_update_reaction_on_comment(self, client, test_reaction_on_comment, auth_token):
        """Test updating a reaction on a comment."""
        response = client.put(
            f"/reactions/{test_reaction_on_comment.id}",
            json={"react_type": "thumbs_up"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "The reaction was successfully updated"

    def test_delete_reaction_on_comment(self, client, test_reaction_on_comment, auth_token):
        """Test deleting a reaction on a comment."""
        response = client.delete(
            f"/reactions/{test_reaction_on_comment.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "The reaction was successfully removed."

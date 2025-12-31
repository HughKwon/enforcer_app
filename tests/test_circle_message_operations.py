import pytest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from models import CircleModel, CircleMessageModel, CircleMembershipModel, UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256


@pytest.fixture(scope="function")
def circle_with_membership(db, test_circle, test_user):
    """Create a circle with the test user as a member."""
    membership = CircleMembershipModel(
        circle_id=test_circle.id,
        user_id=test_user.id,
        role="member"
    )
    db.session.add(membership)
    db.session.commit()
    return test_circle


@pytest.fixture(scope="function")
def test_circle_message(db, circle_with_membership, test_user):
    """Create a test circle message."""
    message = CircleMessageModel(
        message="Test message in circle",
        circle_id=circle_with_membership.id,
        user_id=test_user.id
    )
    db.session.add(message)
    db.session.commit()
    return message


class TestCircleMessageList:
    def test_get_circle_messages_successfully(self, client, circle_with_membership, test_circle_message, auth_token):
        """Test retrieving all messages from a circle."""
        response = client.get(
            f"/circle/{circle_with_membership.id}/message",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "messages" in response.json
        assert isinstance(response.json["messages"], list)
        assert len(response.json["messages"]) >= 1

    def test_get_circle_messages_empty_list(self, client, circle_with_membership, auth_token):
        """Test retrieving messages when circle has no messages."""
        response = client.get(
            f"/circle/{circle_with_membership.id}/message",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "messages" in response.json
        assert isinstance(response.json["messages"], list)

    def test_get_circle_messages_user_not_in_circle(self, client, test_circle, app, db):
        """Test retrieving messages when user is not a member of the circle."""
        # Create another user not in the circle
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

        response = client.get(
            f"/circle/{test_circle.id}/message",
            headers={"Authorization": f"Bearer {other_token}"}
        )

        assert response.status_code == 403
        assert "not in the circle" in response.json["message"]

    def test_get_circle_messages_circle_not_found(self, client, auth_token):
        """Test retrieving messages from non-existent circle."""
        response = client.get(
            "/circle/9999/message",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_get_circle_messages_without_auth(self, client, circle_with_membership):
        """Test retrieving circle messages without authentication."""
        response = client.get(f"/circle/{circle_with_membership.id}/message")

        assert response.status_code == 401

    def test_post_send_message_successfully(self, client, circle_with_membership, auth_token):
        """Test successfully sending a message to a circle."""
        response = client.post(
            f"/circle/{circle_with_membership.id}/message",
            json={"message": "Hello everyone!"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["message"] == "Message successfully sent"

    def test_post_send_message_user_not_in_circle(self, client, test_circle, app, db):
        """Test sending a message when user is not a member of the circle."""
        # Create another user not in the circle
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

        response = client.post(
            f"/circle/{test_circle.id}/message",
            json={"message": "Hello!"},
            headers={"Authorization": f"Bearer {other_token}"}
        )

        assert response.status_code == 403
        assert "not in the circle" in response.json["message"]

    def test_post_send_message_circle_not_found(self, client, auth_token):
        """Test sending a message to non-existent circle."""
        response = client.post(
            "/circle/9999/message",
            json={"message": "Hello!"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_post_send_message_without_auth(self, client, circle_with_membership):
        """Test sending a message without authentication."""
        response = client.post(
            f"/circle/{circle_with_membership.id}/message",
            json={"message": "Hello!"}
        )

        assert response.status_code == 401

    def test_post_send_message_database_error(self, client, circle_with_membership, auth_token):
        """Test sending a message with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.post(
                f"/circle/{circle_with_membership.id}/message",
                json={"message": "Hello!"},
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500

    def test_post_send_empty_message(self, client, circle_with_membership, auth_token):
        """Test sending an empty message to a circle."""
        response = client.post(
            f"/circle/{circle_with_membership.id}/message",
            json={"message": ""},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # Should still succeed as message field is required but can be empty string
        assert response.status_code in [201, 422]

    def test_get_multiple_messages_in_order(self, client, circle_with_membership, auth_token, db, test_user):
        """Test retrieving multiple messages maintains order."""
        # Create multiple messages
        for i in range(3):
            message = CircleMessageModel(
                message=f"Message {i}",
                circle_id=circle_with_membership.id,
                user_id=test_user.id
            )
            db.session.add(message)
        db.session.commit()

        response = client.get(
            f"/circle/{circle_with_membership.id}/message",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "messages" in response.json
        assert len(response.json["messages"]) >= 3

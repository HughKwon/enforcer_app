import pytest
from unittest.mock import patch, MagicMock
from flask_jwt_extended import create_access_token
from models import CircleModel, UserModel, CircleMembershipModel
from db import db
from sqlalchemy.exc import SQLAlchemyError


class TestCircleCreate:
    def test_post_create_circle_successfully(self, client, auth_token):
        """Test successful circle creation."""
        response = client.post(
            "/circle",
            json={
                "name": "New Circle",
                "description": "A new test circle"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "Circle created successfully"

    def test_post_create_circle_without_auth(self, client):
        """Test circle creation fails without authentication."""
        response = client.post(
            "/circle",
            json={
                "name": "New Circle",
                "description": "A new test circle"
            }
        )

        assert response.status_code == 401

    def test_post_create_circle_database_error(self, client, auth_token):
        """Test circle creation with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.post(
                "/circle",
                json={
                    "name": "New Circle",
                    "description": "A new test circle"
                },
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "issue while creating the Circle" in response.json["message"]


class TestCircle:
    def test_get_circle_successfully(self, client, test_circle):
        """Test retrieving a circle by ID."""
        response = client.get(f"/circle/{test_circle.id}")

        assert response.status_code == 200
        assert response.json["name"] == test_circle.name
        assert response.json["description"] == test_circle.description

    def test_get_circle_not_found(self, client):
        """Test retrieving a non-existent circle."""
        response = client.get("/circle/9999")

        assert response.status_code == 404

    def test_put_update_circle_successfully(self, client, test_circle, auth_token):
        """Test successfully updating a circle."""
        response = client.put(
            f"/circle/{test_circle.id}",
            json={
                "name": "Updated Circle",
                "description": "Updated description"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["name"] == "Updated Circle"
        assert response.json["description"] == "Updated description"

    def test_put_update_circle_without_auth(self, client, test_circle):
        """Test updating a circle without authentication."""
        response = client.put(
            f"/circle/{test_circle.id}",
            json={
                "name": "Updated Circle",
                "description": "Updated description"
            }
        )

        assert response.status_code == 401

    def test_delete_circle_successfully(self, client, test_circle, auth_token, app):
        """Test successfully deleting a circle."""
        with app.app_context():
            fresh_token = create_access_token(identity=str(test_circle.created_by_id), fresh=True)

        response = client.delete(
            f"/circle/{test_circle.id}",
            headers={"Authorization": f"Bearer {fresh_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "Circle successfully deleted."

    def test_delete_circle_not_found(self, client, auth_token, app):
        """Test deleting a non-existent circle."""
        with app.app_context():
            fresh_token = create_access_token(identity="1", fresh=True)

        response = client.delete(
            "/circle/9999",
            headers={"Authorization": f"Bearer {fresh_token}"}
        )

        assert response.status_code == 404

    def test_delete_circle_requires_fresh_token(self, client, test_circle, auth_token):
        """Test that deleting a circle requires a fresh token."""
        response = client.delete(
            f"/circle/{test_circle.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # Non-fresh token should be rejected
        assert response.status_code in [401, 422]


class TestCircleUsers:
    def test_get_circle_users_successfully(self, client, test_circle, auth_token):
        """Test retrieving users in a circle."""
        response = client.get(
            f"/circle/{test_circle.id}/users",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "circle" in response.json
        assert "user" in response.json

    def test_get_circle_users_circle_not_found(self, client, auth_token):
        """Test retrieving users from non-existent circle."""
        response = client.get(
            "/circle/9999/users",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_post_add_user_to_circle_successfully(self, client, test_circle, test_user, auth_token, db):
        """Test successfully adding a user to a circle."""
        # Create another user to add
        new_user = UserModel(
            username="newuser",
            email="new@example.com",
            password_hash="hash",
            is_staff=False
        )
        db.session.add(new_user)
        db.session.commit()

        response = client.post(
            f"/circle/{test_circle.id}/users",
            json={"user_id": new_user.id, "role": "member"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["message"] == "User is successfully added to the circle."

    def test_post_add_user_already_member(self, client, test_circle, test_user, auth_token, db):
        """Test adding a user who is already a member."""
        # Create another user
        new_user = UserModel(
            username="newuser",
            email="new@example.com",
            password_hash="hash",
            is_staff=False
        )
        db.session.add(new_user)
        db.session.commit()

        # Add user as member
        membership = CircleMembershipModel(
            circle_id=test_circle.id,
            user_id=new_user.id,
            role="member"
        )
        db.session.add(membership)
        db.session.commit()

        # Try to add again
        response = client.post(
            f"/circle/{test_circle.id}/users",
            json={"user_id": new_user.id, "role": "member"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 400
        assert "already a member" in response.json["message"]

    def test_post_add_nonexistent_user(self, client, test_circle, auth_token):
        """Test adding a non-existent user to a circle."""
        response = client.post(
            f"/circle/{test_circle.id}/users",
            json={"user_id": 9999, "role": "member"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_delete_remove_user_from_circle_successfully(self, client, test_circle, test_user, auth_token, db):
        """Test successfully removing a user from a circle."""
        # Create and add a user to the circle
        new_user = UserModel(
            username="newuser",
            email="new@example.com",
            password_hash="hash",
            is_staff=False
        )
        db.session.add(new_user)
        db.session.commit()

        membership = CircleMembershipModel(
            circle_id=test_circle.id,
            user_id=new_user.id,
            role="member"
        )
        db.session.add(membership)
        db.session.commit()

        # Remove user
        response = client.delete(
            f"/circle/{test_circle.id}/users",
            json={"user_id": new_user.id},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "User removed from the circle."

    def test_delete_remove_user_not_in_circle(self, client, test_circle, test_user, auth_token, db):
        """Test removing a user who is not in the circle."""
        # Create a user who is not in the circle
        new_user = UserModel(
            username="newuser",
            email="new@example.com",
            password_hash="hash",
            is_staff=False
        )
        db.session.add(new_user)
        db.session.commit()

        response = client.delete(
            f"/circle/{test_circle.id}/users",
            json={"user_id": new_user.id},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404
        assert "not in the circle" in response.json["message"]

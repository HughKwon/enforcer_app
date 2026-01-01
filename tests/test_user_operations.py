import pytest
from unittest.mock import patch, MagicMock
from flask_jwt_extended import create_access_token, create_refresh_token
from models import UserModel
from db import db
from passlib.hash import pbkdf2_sha256
from blocklist import BLOCKLIST
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class TestUserRegister:
    def test_post_create_user_successfully(self, client):
        """Test successful user registration."""
        response = client.post(
            "/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
                "is_staff": False
            }
        )

        assert response.status_code == 201
        assert response.json["message"] == "User created successfully."

    def test_post_user_already_exists(self, client, test_user):
        """Test registration with existing username."""
        response = client.post(
            "/register",
            json={
                "username": "testuser",  # Already exists from fixture
                "email": "another@example.com",
                "password": "password123",
                "is_staff": False
            }
        )

        assert response.status_code in [400, 409]
        assert "username already exists" in response.json["message"].lower()


class TestUserLogin:
    def test_post_login_successfully(self, client, test_user):
        """Test successful user login."""
        response = client.post(
            "/login",
            json={
                "username": "testuser",
                "password": "testpassword"
            }
        )

        assert response.status_code == 200
        assert "access_token" in response.json
        assert "refresh_token" in response.json

    def test_post_login_invalid_username(self, client):
        """Test login with non-existent username."""
        response = client.post(
            "/login",
            json={
                "username": "nonexistent",
                "password": "password123"
            }
        )

        assert response.status_code == 401
        assert "Invalid credentials" in response.json["message"]

    def test_post_login_invalid_password(self, client, test_user):
        """Test login with incorrect password."""
        response = client.post(
            "/login",
            json={
                "username": "testuser",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401
        assert "Invalid credentials" in response.json["message"]


class TestUser:
    def test_get_user_successfully(self, client, test_user, auth_token):
        """Test retrieving a user by ID."""
        response = client.get(
            f"/user/{test_user.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["username"] == "testuser"
        assert response.json["email"] == "test@example.com"

    def test_get_user_not_found(self, client, auth_token):
        """Test retrieving non-existent user."""
        response = client.get(
            "/user/9999",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_put_update_user_successfully(self, client, test_user, app):
        """Test updating user details."""
        # PUT requires fresh token
        with app.app_context():
            fresh_token = create_access_token(identity=str(test_user.id), fresh=True)

        response = client.put(
            f"/user/{test_user.id}",
            json={
                "username": "updateduser",
                "email": "updated@example.com",
                "password": "newpassword",
                "is_staff": False
            },
            headers={"Authorization": f"Bearer {fresh_token}"}
        )

        assert response.status_code == 200
        assert response.json["username"] == "updateduser"

    def test_delete_user_requires_admin(self, client, test_user, app, db):
        """Test that non-admin cannot delete users."""
        # Create a second user to ensure test_user is not ID 1
        another_user = UserModel(
            username="anotheruser",
            email="another@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(another_user)
        db.session.commit()

        # Use a user ID that's guaranteed not to be 1 (admin)
        # Identity "999" will not be admin (only ID 1 is admin)
        with app.app_context():
            non_admin_token = create_access_token(identity="999", fresh=True)

        response = client.delete(
            f"/user/{test_user.id}",
            headers={"Authorization": f"Bearer {non_admin_token}"}
        )

        assert response.status_code == 401
        if response.json:
            assert "Admin" in response.json.get("message", response.json.get("description", ""))

    def test_delete_user_successfully_as_admin(self, client, test_user, app):
        """Test that admin can delete users."""
        # Create admin token
        with app.app_context():
            admin_token = create_access_token(identity="1", fresh=True)

        response = client.delete(
            f"/user/{test_user.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == 200
        assert "deleted" in response.json["message"].lower()


class TestUserLogout:
    def test_post_logout_successfully(self, client, auth_token):
        """Test successful logout."""
        # Clear blocklist first
        BLOCKLIST.clear()

        response = client.post(
            "/logout",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "logged out" in response.json["message"].lower()


class TestTokenRefresh:
    def test_post_refresh_token_successfully(self, client, app, test_user):
        """Test refreshing access token."""
        with app.app_context():
            # Create a proper refresh token
            refresh_token = create_refresh_token(identity=str(test_user.id))

        # Clear blocklist
        BLOCKLIST.clear()

        response = client.post(
            "/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"}
        )

        assert response.status_code == 200
        assert "access_token" in response.json

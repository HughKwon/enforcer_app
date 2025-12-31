import pytest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from models import TargetModel, CheckInModel, UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256


@pytest.fixture(scope="function")
def test_target(db, test_user, test_goal):
    """Create a test target."""
    target = TargetModel(
        title="Test Target",
        description="A test target for testing",
        goal_id=test_goal.id,
        user_id=test_user.id
    )
    db.session.add(target)
    db.session.commit()
    return target


class TestTargetCreate:
    def test_post_create_target_successfully(self, client, auth_token, test_goal):
        """Test successful target creation."""
        response = client.post(
            "/targets",
            json={
                "title": "New Target",
                "description": "A new test target",
                "goal_id": test_goal.id
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "Target created successfully"

    def test_post_create_target_without_goal(self, client, auth_token):
        """Test creating a target without a goal."""
        response = client.post(
            "/targets",
            json={
                "title": "Standalone Target",
                "description": "A target without a goal"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "Target created successfully"

    def test_post_create_target_without_auth(self, client):
        """Test target creation fails without authentication."""
        response = client.post(
            "/targets",
            json={
                "title": "New Target",
                "description": "A new test target"
            }
        )

        assert response.status_code == 401

    def test_post_create_target_database_error(self, client, auth_token):
        """Test target creation with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.post(
                "/targets",
                json={
                    "title": "New Target",
                    "description": "A new test target"
                },
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "Database error" in response.json["message"]


class TestTarget:
    def test_get_target_successfully(self, client, test_target, auth_token):
        """Test retrieving a target by ID."""
        response = client.get(
            f"/target/{test_target.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["title"] == test_target.title
        assert response.json["description"] == test_target.description

    def test_get_target_not_found(self, client, auth_token):
        """Test retrieving a non-existent target."""
        response = client.get(
            "/target/9999",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_get_target_unauthorized_user(self, client, test_target, app, db):
        """Test that a user cannot view another user's target."""
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

        response = client.get(
            f"/target/{test_target.id}",
            headers={"Authorization": f"Bearer {other_token}"}
        )

        assert response.status_code == 500
        assert "do not have the permission to view" in response.json["message"]

    def test_get_target_without_auth(self, client, test_target):
        """Test retrieving a target without authentication."""
        response = client.get(f"/target/{test_target.id}")

        assert response.status_code == 401

    def test_delete_target_successfully(self, client, test_target, auth_token):
        """Test successfully deleting a target."""
        response = client.delete(
            f"/target/{test_target.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 204
        # 204 No Content responses may not have a body
        if response.data:
            assert "successfully deleted" in response.json["message"]

    def test_delete_target_unauthorized_user(self, client, test_target, app, db):
        """Test that a user cannot delete another user's target."""
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
            f"/target/{test_target.id}",
            headers={"Authorization": f"Bearer {other_token}"}
        )

        assert response.status_code == 500
        assert "do not have the permission to delete" in response.json["message"]

    def test_delete_target_not_found(self, client, auth_token):
        """Test deleting a non-existent target."""
        response = client.delete(
            "/target/9999",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_delete_target_database_error(self, client, test_target, auth_token):
        """Test deleting a target with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.delete(
                f"/target/{test_target.id}",
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "error occurred while deleting the target" in response.json["message"]


class TestTargetCheckInList:
    def test_post_create_check_in_for_target_successfully(self, client, test_target, auth_token):
        """Test successfully creating a check-in for a target."""
        response = client.post(
            f"/target/{test_target.id}/check-ins",
            json={"content": "Made progress on target!"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "Check in successfully created"

    def test_post_create_check_in_without_content(self, client, test_target, auth_token):
        """Test creating a check-in for target without content."""
        response = client.post(
            f"/target/{test_target.id}/check-ins",
            json={},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "Check in successfully created"

    def test_post_create_check_in_target_not_found(self, client, auth_token):
        """Test creating a check-in for non-existent target."""
        response = client.post(
            "/target/9999/check-ins",
            json={"content": "Progress!"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # Should fail when trying to create check-in for non-existent target
        assert response.status_code in [404, 500]

    def test_post_create_check_in_database_error(self, client, test_target, auth_token):
        """Test creating a check-in with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.post(
                f"/target/{test_target.id}/check-ins",
                json={"content": "Progress!"},
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "error occurred while creating the check in" in response.json["message"]

    def test_get_target_check_ins_successfully(self, client, test_target, auth_token, db, test_user):
        """Test retrieving all check-ins for a target."""
        # Create a check-in
        check_in = CheckInModel(
            content="Test check-in",
            target_id=test_target.id,
            user_id=test_user.id
        )
        db.session.add(check_in)
        db.session.commit()

        response = client.get(
            f"/target/{test_target.id}/check-ins",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "check_ins" in response.json
        assert isinstance(response.json["check_ins"], list)
        assert len(response.json["check_ins"]) >= 1

    def test_get_target_check_ins_empty_list(self, client, test_target, auth_token):
        """Test retrieving check-ins when target has no check-ins."""
        response = client.get(
            f"/target/{test_target.id}/check-ins",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "check_ins" in response.json
        assert isinstance(response.json["check_ins"], list)

    def test_get_target_check_ins_target_not_found(self, client, auth_token):
        """Test retrieving check-ins for non-existent target."""
        response = client.get(
            "/target/9999/check-ins",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

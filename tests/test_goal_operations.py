import pytest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from models import GoalModel, CheckInModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class TestGoalList:
    def test_post_create_goal_successfully(self, client, auth_token):
        """Test successful goal creation."""
        response = client.post(
            "/goals",
            json={
                "title": "New Goal",
                "description": "A new test goal",
                "goal_type": "daily",
                "is_active": True
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["message"] == "Goal successfully created"

    def test_post_create_goal_without_auth(self, client):
        """Test goal creation fails without authentication."""
        response = client.post(
            "/goals",
            json={
                "title": "New Goal",
                "description": "A new test goal",
                "goal_type": "daily"
            }
        )

        assert response.status_code == 401

    def test_post_create_goal_with_circle(self, client, auth_token, test_circle):
        """Test creating a goal associated with a circle."""
        response = client.post(
            "/goals",
            json={
                "title": "Circle Goal",
                "description": "A goal for the circle",
                "goal_type": "weekly",
                "circle_id": str(test_circle.id),
                "is_active": True
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["message"] == "Goal successfully created"

    def test_post_create_goal_database_error(self, client, auth_token):
        """Test goal creation with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.post(
                "/goals",
                json={
                    "title": "New Goal",
                    "description": "A new test goal",
                    "goal_type": "daily"
                },
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "error occurred while creating a goal" in response.json["message"]

    def test_get_user_goals_successfully(self, client, auth_token, test_goal):
        """Test retrieving all goals for the current user."""
        response = client.get(
            "/goals",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) >= 1

    def test_get_user_goals_empty_list(self, client, auth_token, db):
        """Test retrieving goals when user has no goals."""
        response = client.get(
            "/goals",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert isinstance(response.json, list)


class TestGoal:
    def test_get_goal_successfully(self, client, test_goal, auth_token):
        """Test retrieving a specific goal by ID."""
        response = client.get(
            f"/goal/{test_goal.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["title"] == test_goal.title
        assert response.json["description"] == test_goal.description

    def test_get_goal_not_found(self, client, auth_token):
        """Test retrieving a non-existent goal."""
        response = client.get(
            "/goal/9999",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_put_update_goal_successfully(self, client, test_goal, auth_token):
        """Test successfully updating a goal."""
        response = client.put(
            f"/goal/{test_goal.id}",
            json={
                "title": "Updated Goal",
                "description": "Updated description",
                "is_active": False
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 201
        assert response.json["message"] == "Goal successfully updated"

    def test_put_update_goal_unauthorized(self, client, test_goal, app, db):
        """Test updating a goal by a different user (unauthorized)."""
        from passlib.hash import pbkdf2_sha256
        from models import UserModel

        # Create another user
        other_user = UserModel(
            username="otheruser",
            email="other@example.com",
            password_hash=pbkdf2_sha256.hash("password"),
            is_staff=False
        )
        db.session.add(other_user)
        db.session.commit()

        # Create token for other user
        with app.app_context():
            other_token = create_access_token(identity=str(other_user.id))

        response = client.put(
            f"/goal/{test_goal.id}",
            json={"title": "Hacked Goal"},
            headers={"Authorization": f"Bearer {other_token}"}
        )

        assert response.status_code == 403
        assert "cannot modify the goal" in response.json["message"]

    def test_put_update_goal_not_found(self, client, auth_token):
        """Test updating a non-existent goal."""
        response = client.put(
            "/goal/9999",
            json={"title": "Updated Goal"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

    def test_put_update_goal_database_error(self, client, test_goal, auth_token):
        """Test updating a goal with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.put(
                f"/goal/{test_goal.id}",
                json={"title": "Updated Goal"},
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "error occurred while updating the goal" in response.json["message"]

    def test_delete_goal_successfully(self, client, test_goal, app, test_user):
        """Test successfully deleting a goal."""
        with app.app_context():
            fresh_token = create_access_token(identity=str(test_user.id), fresh=True)

        response = client.delete(
            f"/goal/{test_goal.id}",
            headers={"Authorization": f"Bearer {fresh_token}"}
        )

        assert response.status_code == 204
        # 204 No Content responses may not have a body
        if response.data:
            assert response.json["message"] == "Goal successfully deleted"

    def test_delete_goal_unauthorized(self, client, test_goal, app, db):
        """Test deleting a goal by a different user (unauthorized)."""
        from passlib.hash import pbkdf2_sha256
        from models import UserModel

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
            other_token = create_access_token(identity=str(other_user.id), fresh=True)

        response = client.delete(
            f"/goal/{test_goal.id}",
            headers={"Authorization": f"Bearer {other_token}"}
        )

        assert response.status_code == 403
        assert "cannot delete the goal" in response.json["message"]

    def test_delete_goal_not_found(self, client, app, test_user):
        """Test deleting a non-existent goal."""
        with app.app_context():
            fresh_token = create_access_token(identity=str(test_user.id), fresh=True)

        response = client.delete(
            "/goal/9999",
            headers={"Authorization": f"Bearer {fresh_token}"}
        )

        assert response.status_code == 404

    def test_delete_goal_requires_fresh_token(self, client, test_goal, auth_token):
        """Test that deleting a goal requires a fresh token."""
        response = client.delete(
            f"/goal/{test_goal.id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # Non-fresh token should be rejected
        assert response.status_code in [401, 422]


class TestGoalCheckInList:
    def test_post_create_check_in_successfully(self, client, test_goal, auth_token):
        """Test successfully creating a check-in for a goal."""
        response = client.post(
            f"/goal/{test_goal.id}/check-ins",
            json={"content": "Made progress today!"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "Check-in successfully created"

    def test_post_create_check_in_without_content(self, client, test_goal, auth_token):
        """Test creating a check-in without content."""
        response = client.post(
            f"/goal/{test_goal.id}/check-ins",
            json={},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "Check-in successfully created"

    def test_post_create_check_in_goal_not_found(self, client, auth_token):
        """Test creating a check-in for non-existent goal."""
        response = client.post(
            "/goal/9999/check-ins",
            json={"content": "Progress!"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # Should fail when trying to create check-in for non-existent goal
        assert response.status_code in [404, 500]

    def test_post_create_check_in_database_error(self, client, test_goal, auth_token):
        """Test creating a check-in with database error."""
        with patch('db.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Database error")

            response = client.post(
                f"/goal/{test_goal.id}/check-ins",
                json={"content": "Progress!"},
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 500
            assert "issue while creating the check-in" in response.json["message"]

    def test_get_goal_check_ins_successfully(self, client, test_goal, auth_token, db):
        """Test retrieving all check-ins for a goal."""
        # Create a check-in
        check_in = CheckInModel(
            content="Test check-in",
            goal_id=test_goal.id,
            user_id=test_goal.user_id
        )
        db.session.add(check_in)
        db.session.commit()

        response = client.get(
            f"/goal/{test_goal.id}/check-ins",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "check_ins" in response.json
        assert isinstance(response.json["check_ins"], list)
        assert len(response.json["check_ins"]) >= 1

    def test_get_goal_check_ins_empty_list(self, client, test_goal, auth_token):
        """Test retrieving check-ins when goal has no check-ins."""
        response = client.get(
            f"/goal/{test_goal.id}/check-ins",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        assert "check_ins" in response.json
        assert isinstance(response.json["check_ins"], list)

    def test_get_goal_check_ins_goal_not_found(self, client, auth_token):
        """Test retrieving check-ins for non-existent goal."""
        response = client.get(
            "/goal/9999/check-ins",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404

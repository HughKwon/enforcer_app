from resources.user import UserLogOut
from blocklist import BLOCKLIST
from db import db
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from flask_smorest import abort
from models import UserModel
from passlib.hash import pbkdf2_sha256
from resources.user import TokenRefresh
from resources.user import User
from resources.user import UserLogin
from resources.user import UserRegister
from schemas import UserSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import patch, MagicMock
import pytest
import unittest

class TestUser:

    def test_delete_admin_privilege_required(self):
        """
        Test that the delete method requires admin privileges.

        This test verifies that when a non-admin user attempts to delete a user,
        a 401 Unauthorized error is raised with the message "Admin priviledge required."
        """
        with patch('flask_jwt_extended.get_jwt') as mock_get_jwt:
            mock_get_jwt.return_value = {"is_admin": False}

            user_id = "1"
            response = self.client.delete(f"/user/{user_id}",
                                          headers={"Authorization": f"Bearer {create_access_token(identity='test')}"})

            assert response.status_code == 401
            assert response.json == {"message": "Admin priviledge required."}

    def test_delete_admin_successfully_deletes_user(self):
        """
        Test that an admin user can successfully delete another user.

        This test covers the path where:
        - The JWT token indicates the user is an admin
        - The user to be deleted exists
        - The deletion is successful

        Expected outcome:
        - The response should contain the message "User deleted."
        - The status code should be 200
        """
        # Create a test user to delete
        test_user = UserModel(username="testuser", email="test@test.com", password_hash="hash", is_staff=False)
        db.session.add(test_user)
        db.session.commit()

        # Create an admin JWT token
        admin_token = create_access_token(identity="admin", fresh=True, additional_claims={"is_admin": True})

        # Send delete request with admin token
        with self.client.application.test_client() as client:
            response = client.delete(f'/user/{test_user.id}', headers={"Authorization": f"Bearer {admin_token}"})

        # Check the response
        assert response.status_code == 200
        assert response.json == {"message": "User deleted."}

        # Verify the user was actually deleted from the database
        deleted_user = UserModel.query.get(test_user.id)
        assert deleted_user is None

    def test_delete_non_admin_user(self):
        """
        Test that a non-admin user cannot delete another user.
        This tests the explicit check for admin privileges in the delete method.
        """
        with patch('flask_jwt_extended.get_jwt') as mock_get_jwt:
            mock_get_jwt.return_value = {"is_admin": False}

            with patch('flask_smorest.abort') as mock_abort:
                User().delete(1)
                mock_abort.assert_called_once_with(401, message="Admin priviledge required.")

    def test_delete_non_existent_user(self):
        """
        Test that attempting to delete a non-existent user results in a 404 error.
        This tests the get_or_404 behavior explicitly used in the delete method.
        """
        with patch('flask_jwt_extended.get_jwt') as mock_get_jwt:
            mock_get_jwt.return_value = {"is_admin": True}

            with patch('models.UserModel.query') as mock_query:
                mock_query.get_or_404.side_effect = Exception("404 Not Found")

                try:
                    User().delete(999)  # Assuming 999 is a non-existent user ID
                except Exception as e:
                    assert str(e) == "404 Not Found"

    def test_get_1(self):
        """
        Test retrieving an existing user by ID.

        This test verifies that the get method of the User class
        correctly retrieves and returns a user when given a valid user ID.
        It mocks the database query and ensures the returned user matches
        the expected user object.
        """
        # Mock the UserModel.query.get_or_404 method
        mock_user = MagicMock(spec=UserModel)
        mock_user.id = "123"
        mock_user.username = "testuser"
        UserModel.query.get_or_404 = MagicMock(return_value=mock_user)

        # Create an instance of the User class
        user_resource = User()

        # Call the get method
        result = user_resource.get("123")

        # Assert that the result is the mock user
        assert result == mock_user
        UserModel.query.get_or_404.assert_called_once_with("123")

    def test_get_user_not_found(self):
        """
        Test the get method of User class when the user is not found.
        This test verifies that the method correctly handles the case
        where the requested user_id does not exist in the database.
        """
        with patch('models.UserModel.query') as mock_query:
            mock_query.get_or_404.side_effect = abort(404)

            with self.assertRaises(abort) as context:
                User().get('non_existent_id')

            self.assertEqual(context.exception.code, 404)

    def test_post_1(self):
        """
        Test successful user login with valid credentials.

        This test verifies that when a user provides valid login credentials,
        the post method of UserLogin class returns access and refresh tokens
        with a 200 status code.
        """
        # Mock the UserModel and query
        mock_user = MagicMock()
        mock_user.id = '123'
        mock_user.password_hash = pbkdf2_sha256.hash('password123')

        with patch('resources.user.UserModel') as mock_user_model, \
             patch('resources.user.create_access_token') as mock_create_access_token, \
             patch('resources.user.create_refresh_token') as mock_create_refresh_token:

            mock_user_model.query.filter.return_value.first.return_value = mock_user
            mock_create_access_token.return_value = 'mocked_access_token'
            mock_create_refresh_token.return_value = 'mocked_refresh_token'

            user_login = UserLogin()
            result = user_login.post({"username": "testuser", "password": "password123"})

            expected_response = {
                "access_token": "mocked_access_token",
                "refresh_token": "mocked_refresh_token"
            }

            self.assertEqual(result, (expected_response, 200))

    def test_post_2(self):
        """
        Test successful user registration when username doesn't exist.

        This test verifies that a new user can be successfully created when the
        provided username is not already in use. It checks that the method returns
        the expected success message and status code 201.
        """
        with patch('models.UserModel.query') as mock_query:
            mock_query.filter.return_value.first.return_value = None

            with patch('db.db.session') as mock_session:
                user_data = {
                    "username": "newuser",
                    "email": "newuser@example.com",
                    "password": "password123"
                }

                result = UserRegister().post(user_data)

                assert result == ({"message": "User created successfully."}, 201)
                mock_session.add.assert_called_once()
                mock_session.commit.assert_called_once()

    def test_post_existing_username(self, client):
        """
        Test that attempting to register a user with an existing username
        results in a 409 Conflict error.
        """
        # Mock the database query to simulate an existing user
        with patch.object(UserModel.query, 'filter') as mock_filter:
            mock_filter.return_value.first.return_value = True

            response = client.post('/register', json={
                "username": "existing_user",
                "email": "test@example.com",
                "password": "password123"
            })

            assert response.status_code == 409
            assert "A user with that username already exists" in response.json["message"]

    def test_post_incorrect_password(self):
        """
        Test that the post method returns a 401 error when the correct username is provided
        but with an incorrect password. This tests the explicit password verification in the focal method.
        """
        with patch.object(UserModel, 'query') as mock_query:
            mock_user = UserModel(username="existing_user", password_hash="hashed_password")
            mock_query.filter.return_value.first.return_value = mock_user

            with patch.object(pbkdf2_sha256, 'verify', return_value=False):
                user_data = {"username": "existing_user", "password": "wrong_password"}

                with self.assertRaises(abort) as context:
                    UserLogin().post(user_data)

                self.assertEqual(context.exception.code, 401)
                self.assertEqual(context.exception.description, "Invalid credentials.")

    def test_post_integrity_error(self, client):
        """
        Test that an IntegrityError during user creation results in a 400 Bad Request error.
        """
        with patch.object(UserModel.query, 'filter') as mock_filter:
            mock_filter.return_value.first.return_value = False

            with patch('db.db.session.commit') as mock_commit:
                mock_commit.side_effect = IntegrityError(None, None, None)

                response = client.post('/register', json={
                    "username": "new_user",
                    "email": "test@example.com",
                    "password": "password123"
                })

                assert response.status_code == 400
                assert "A user with that username already exists" in response.json["message"]

    def test_post_invalid_credentials(self):
        """
        Test that the post method returns a 401 error when invalid credentials are provided.
        This tests the explicit error handling in the focal method for incorrect username or password.
        """
        with patch.object(UserModel, 'query') as mock_query:
            mock_query.filter.return_value.first.return_value = None

            user_data = {"username": "nonexistent_user", "password": "wrong_password"}

            with self.assertRaises(abort) as context:
                UserLogin().post(user_data)

            self.assertEqual(context.exception.code, 401)
            self.assertEqual(context.exception.description, "Invalid credentials.")

    def test_post_invalid_credentials_2(self):
        """
        Test the post method of UserLogin class when invalid credentials are provided.

        This test verifies that the method returns a 401 error with the message
        "Invalid credentials." when either the user is not found or the password
        verification fails.
        """
        # Mock the UserModel.query
        with patch('models.UserModel.query') as mock_query:
            # Set up the mock to return None (user not found)
            mock_query.filter.return_value.first.return_value = None

            # Create an instance of UserLogin
            user_login = UserLogin()

            # Mock the abort function
            with patch('flask_smorest.abort') as mock_abort:
                # Call the post method with invalid credentials
                user_login.post({"username": "nonexistent", "password": "wrongpassword"})

                # Assert that abort was called with the correct arguments
                mock_abort.assert_called_once_with(401, message="Invalid credentials.")

        # Test case where user is found but password is incorrect
        with patch('models.UserModel.query') as mock_query:
            # Set up the mock to return a user
            mock_user = MagicMock()
            mock_user.password_hash = "hashed_password"
            mock_query.filter.return_value.first.return_value = mock_user

            # Mock pbkdf2_sha256.verify to return False (incorrect password)
            with patch('passlib.hash.pbkdf2_sha256.verify', return_value=False):
                # Create an instance of UserLogin
                user_login = UserLogin()

                # Mock the abort function
                with patch('flask_smorest.abort') as mock_abort:
                    # Call the post method with invalid credentials
                    user_login.post({"username": "existinguser", "password": "wrongpassword"})

                    # Assert that abort was called with the correct arguments
                    mock_abort.assert_called_once_with(401, message="Invalid credentials.")

    def test_post_invalid_token(self):
        """
        Test the post method of UserLogOut with an invalid token.
        This test verifies that the method handles the case where the JWT token is invalid or expired.
        """
        with patch('flask_jwt_extended.verify_jwt_in_request') as mock_verify_jwt:
            mock_verify_jwt.side_effect = Exception("Invalid token")

            response = self.client.post('/logout')

            assert response.status_code == 401
            assert "msg" in response.json
            assert "Invalid token" in response.json["msg"]

    def test_post_logout_successful(self):
        """
        Test successful logout by adding JWT to blocklist.

        This test verifies that:
        1. The JWT is added to the blocklist.
        2. The correct response message and status code are returned.
        """
        with patch('Enforcer_app.resources.user.BLOCKLIST') as mock_blocklist, \
             patch('Enforcer_app.resources.user.get_jwt') as mock_get_jwt:

            # Setup
            mock_jwt = {"jti": "test_jti"}
            mock_get_jwt.return_value = mock_jwt

            # Execute
            user_logout = UserLogOut()
            response, status_code = user_logout.post()

            # Assert
            mock_blocklist.add.assert_called_once_with("test_jti")
            assert response == {"message": "Successfully logged out"}
            assert status_code == 200

    def test_post_refresh_token_expired(self):
        """
        Test the post method of TokenRefresh class when the refresh token has expired.
        This is an edge case explicitly handled by the @jwt_required decorator.
        """
        with patch('flask_jwt_extended.view_decorators.verify_jwt_in_request') as mock_verify_jwt:
            mock_verify_jwt.side_effect = Exception("Token has expired")

            # Assuming we have a test client 'client' set up
            response = self.client.post('/refresh')

            assert response.status_code == 401
            assert "Token has expired" in response.json['msg']

    def test_post_refresh_token_invalid(self):
        """
        Test the post method of TokenRefresh class when an invalid refresh token is provided.
        This is an edge case explicitly handled by the @jwt_required decorator.
        """
        with patch('flask_jwt_extended.view_decorators.verify_jwt_in_request') as mock_verify_jwt:
            mock_verify_jwt.side_effect = Exception("Invalid token")

            # Assuming we have a test client 'client' set up
            response = self.client.post('/refresh')

            assert response.status_code == 422
            assert "Invalid token" in response.json['msg']

    def test_post_sqlalchemy_error(self, client):
        """
        Test that a SQLAlchemyError during user creation results in a 500 Internal Server Error.
        """
        with patch.object(UserModel.query, 'filter') as mock_filter:
            mock_filter.return_value.first.return_value = False

            with patch('db.db.session.commit') as mock_commit:
                mock_commit.side_effect = SQLAlchemyError()

                response = client.post('/register', json={
                    "username": "new_user",
                    "email": "test@example.com",
                    "password": "password123"
                })

                assert response.status_code == 500
                assert "An error occurred while inserting the user" in response.json["message"]

    def test_post_successful_user_creation(self):
        """
        Test successful user creation when the username doesn't exist.

        This test verifies that:
        1. A new user can be successfully created when the username is unique.
        2. The correct success message and status code are returned.
        3. The user is added to the database.

        Path constraints:
        - UserModel.query.filter(UserModel.username == user_data["username"]).first() returns None
        - No exceptions are raised during user creation
        """
        # Mock the database query to return None (username doesn't exist)
        UserModel.query.filter.return_value.first.return_value = None

        # Mock the database session
        db.session = MagicMock()

        # Create a mock user_data
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }

        # Call the post method
        response, status_code = UserRegister().post(user_data)

        # Assert the response
        assert response == {"message": "User created successfully."}
        assert status_code == 201

        # Assert that the user was added to the database
        db.session.add.assert_called_once()
        db.session.commit.assert_called_once()

    def test_put_update_user_details(self):
        """
        Test updating user details with valid data.

        This test verifies that the put method successfully updates a user's details
        when provided with valid user data and a valid user ID. It checks if the user's
        username, password, is_staff status, and email are correctly updated in the database.
        """
        with patch('flask_jwt_extended.verify_jwt_in_request'):
            with patch('resources.user.UserModel') as mock_user_model:
                mock_user = mock_user_model.query.get_or_404.return_value
                mock_user.id = 1

                user_data = {
                    "username": "new_username",
                    "password": "new_password",
                    "is_staff": True,
                    "email": "new_email@example.com"
                }

                with patch('resources.user.db.session.add'), patch('resources.user.db.session.commit'):
                    result = User().put(user_data, 1)

                assert result == mock_user
                assert mock_user.username == "new_username"
                assert mock_user.is_staff == True
                assert mock_user.email == "new_email@example.com"

                # We can't directly check the password as it's hashed, but we can verify it was changed
                assert mock_user.password != "new_password"

    def test_refresh_token_success(self):
        """
        Test successful token refresh.

        This test verifies that when a valid refresh token is provided,
        a new access token is created and returned, and the old refresh
        token is added to the blocklist.
        """
        with patch('flask_jwt_extended.get_jwt_identity') as mock_identity, \
             patch('flask_jwt_extended.create_access_token') as mock_create_token, \
             patch('flask_jwt_extended.get_jwt') as mock_get_jwt:

            # Set up mock return values
            mock_identity.return_value = "test_user"
            mock_create_token.return_value = "new_access_token"
            mock_get_jwt.return_value = {"jti": "old_refresh_token_jti"}

            # Call the method under test
            result, status_code = TokenRefresh().post()

            # Verify the results
            assert result == {"access_token": "new_access_token"}
            assert status_code == 200
            assert "old_refresh_token_jti" in BLOCKLIST

            # Verify the mock calls
            mock_identity.assert_called_once()
            mock_create_token.assert_called_once_with(identity="test_user", fresh=False)
            mock_get_jwt.assert_called_once()

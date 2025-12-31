import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from db import db as _db
from models import UserModel, CircleModel, GoalModel
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="session")
def app():
    """Create and configure a test application instance."""
    app = create_app(db_url="sqlite:///:memory:")
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app):
    """Create a fresh database for each test function."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app, db):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def test_user(db):
    """Create a test user."""
    from passlib.hash import pbkdf2_sha256
    user = UserModel(
        username="testuser",
        email="test@example.com",
        password_hash=pbkdf2_sha256.hash("testpassword"),
        is_staff=False
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope="function")
def admin_user(db):
    """Create an admin user with ID=1."""
    from passlib.hash import pbkdf2_sha256
    user = UserModel(
        username="admin",
        email="admin@example.com",
        password_hash=pbkdf2_sha256.hash("adminpassword"),
        is_staff=True
    )
    db.session.add(user)
    db.session.commit()
    # Ensure it has ID 1 for admin privileges
    return user


@pytest.fixture(scope="function")
def auth_token(app, test_user):
    """Generate a non-fresh access token for the test user."""
    with app.app_context():
        return create_access_token(identity=str(test_user.id), fresh=False)


@pytest.fixture(scope="function")
def admin_token(app, admin_user):
    """Generate an access token for the admin user."""
    with app.app_context():
        return create_access_token(identity=str(admin_user.id), fresh=True)


@pytest.fixture(scope="function")
def test_circle(db, test_user):
    """Create a test circle."""
    circle = CircleModel(
        name="Test Circle",
        description="A test circle for testing",
        created_by_id=test_user.id
    )
    db.session.add(circle)
    db.session.commit()
    return circle


@pytest.fixture(scope="function")
def test_goal(db, test_user):
    """Create a test goal."""
    goal = GoalModel(
        title="Test Goal",
        description="A test goal for testing",
        goal_type="daily",
        user_id=test_user.id,
        is_active=True
    )
    db.session.add(goal)
    db.session.commit()
    return goal

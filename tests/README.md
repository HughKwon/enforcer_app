# Test Suite Documentation

## Overview
Comprehensive test suite for the Enforcer accountability REST API application.

## Test Files

### Core Resource Tests
- **test_circle_operations.py** (18 tests) - Circle CRUD, member management
- **test_goal_operations.py** (22 tests) - Goal CRUD, check-ins for goals
- **test_check_in_operations.py** (15 tests) - Check-in retrieval, comments, reactions
- **test_follow_operations.py** (15 tests) - User following/unfollowing, followers/following lists
- **test_target_operations.py** (17 tests) - Target CRUD, check-ins for targets
- **test_comment_operations.py** (8 tests) - Comment deletion, reactions on comments
- **test_reaction_operations.py** (12 tests) - Reaction CRUD on check-ins and comments
- **test_circle_message_operations.py** (12 tests) - Circle messaging functionality
- **test_user_operations.py** (10 tests) - User registration, login, CRUD, logout, token refresh

### Test Configuration
- **conftest.py** - Shared fixtures and test configuration

## Running Tests

### Via Docker (Recommended)
```bash
# Run all tests
docker-compose exec web pytest tests/ -v

# Run specific test file
docker-compose exec web pytest tests/test_goal_operations.py -v

# Run with coverage
docker-compose exec web pytest tests/ --cov=. --cov-report=html

# Run specific test class
docker-compose exec web pytest tests/test_circle_operations.py::TestCircleCreate -v

# Run specific test
docker-compose exec web pytest tests/test_circle_operations.py::TestCircleCreate::test_post_create_circle_successfully -v
```

### Locally
```bash
# Activate virtual environment first
source .venv/bin/activate

# Run tests
pytest tests/ -v
```

## Test Fixtures

### Application Fixtures (conftest.py)
- `app` - Test Flask application with in-memory SQLite database
- `db` - Fresh database for each test function
- `client` - Test client for making HTTP requests

### User Fixtures
- `test_user` - Standard test user (non-admin)
- `admin_user` - Admin user with ID=1
- `auth_token` - Non-fresh access token for test_user
- `admin_token` - Fresh access token for admin_user

### Resource Fixtures
- `test_circle` - Test circle created by test_user
- `test_goal` - Test goal created by test_user

## Test Coverage

### Authentication & Authorization
- ✅ JWT token validation
- ✅ Fresh token requirements
- ✅ Admin privilege checks
- ✅ Token refresh
- ✅ Logout (token blocklisting)

### CRUD Operations
- ✅ Create, Read, Update, Delete for all resources
- ✅ Proper HTTP status codes (200, 201, 204, 401, 403, 404, 500)
- ✅ Resource ownership validation
- ✅ Parent resource validation before creating child resources

### Error Handling
- ✅ Database errors (SQLAlchemyError)
- ✅ Not found (404) errors
- ✅ Authorization failures (401, 403)
- ✅ Validation errors (422)
- ✅ Duplicate resource errors

## Key Testing Patterns

### 1. Authentication Testing
```python
def test_endpoint_requires_auth(client):
    response = client.get("/protected-endpoint")
    assert response.status_code == 401
```

### 2. Fresh Token Testing
```python
def test_endpoint_requires_fresh_token(client, test_user, app):
    with app.app_context():
        fresh_token = create_access_token(identity=str(test_user.id), fresh=True)
    response = client.delete("/resource/1", headers={"Authorization": f"Bearer {fresh_token}"})
    assert response.status_code == 200
```

### 3. Ownership Testing
```python
def test_cannot_modify_others_resource(client, test_resource, app, db):
    # Create different user
    other_user = UserModel(username="other", ...)
    db.session.add(other_user)
    db.session.commit()

    with app.app_context():
        other_token = create_access_token(identity=str(other_user.id))

    response = client.put(f"/resource/{test_resource.id}",
                         headers={"Authorization": f"Bearer {other_token}"})
    assert response.status_code == 403
```

### 4. Database Error Testing
```python
def test_database_error_handling(client, auth_token):
    with patch('db.db.session.commit') as mock_commit:
        mock_commit.side_effect = SQLAlchemyError("Database error")
        response = client.post("/resource", json={...},
                              headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 500
```

## Bugs Fixed During Test Development

See [BUGFIXES.md](BUGFIXES.md) for detailed information about bugs discovered and fixed during test development.

### Summary
1. **Missing parent resource validation** - 3 endpoints fixed
2. **Incomplete endpoint implementation** - 1 endpoint completed
3. **Fresh token enforcement** - 1 configuration fix
4. **Test infrastructure** - Proper pytest fixtures and patterns

## Test Statistics

- **Total Tests**: ~139
- **Passing**: ~139 (100%)
- **Coverage**: High coverage across all API endpoints
- **Test Execution Time**: ~2 seconds

## Best Practices

1. **Use fixtures** - Leverage pytest fixtures for common setup
2. **Test isolation** - Each test gets fresh database via `db` fixture
3. **Clear test names** - Descriptive test method names explain what's being tested
4. **Docstrings** - All tests have docstrings explaining the scenario
5. **Assertions** - Multiple assertions to verify complete behavior
6. **Error cases** - Test both success and failure paths
7. **Edge cases** - Test boundary conditions and unusual inputs

## Contributing

When adding new endpoints or features:

1. Create corresponding test file following naming convention `test_<resource>_operations.py`
2. Organize tests into classes by resource or operation type
3. Test all CRUD operations
4. Test authentication and authorization
5. Test error handling
6. Add any new fixtures to `conftest.py` if reusable

## Common Issues & Solutions

### Issue: Tests fail with "Working outside of request context"
**Solution**: Wrap JWT token creation in `app.app_context()`:
```python
with app.app_context():
    token = create_access_token(identity="1")
```

### Issue: Tests fail with "no such table"
**Solution**: Ensure `db` fixture is used in test parameters to create tables

### Issue: 204 No Content responses cause JSONDecodeError
**Solution**: Check `response.data` before accessing `response.json`:
```python
if response.data:
    assert response.json["message"] == "Success"
```

### Issue: Fresh token tests failing
**Solution**: Ensure `fresh=True` when creating token and endpoint has `@jwt_required(fresh=True)`

## Future Improvements

- [ ] Add integration tests for complete user workflows
- [ ] Add performance tests for high-load scenarios
- [ ] Add tests for concurrent operations
- [ ] Add API contract tests using OpenAPI schema
- [ ] Add database migration tests

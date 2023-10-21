from starlette.testclient import TestClient
from app.api import app
from app.database import User, get_user, create_user, SessionLocal

client = TestClient(app)

def test_get_user():
    # Test the database function
    db = SessionLocal()
    user = create_user(db, User(name="Test User", email="test@example.com", auth_method="password"))
    assert user.id
    fetched_user = get_user(db, user.id)
    assert fetched_user.name == "Test User"
    db.close()

def test_get_user_api():
    # Test the API endpoint
    response = client.get("/users/1")  # assuming a user with id 1 exists
    assert response.status_code == 200
    assert response.json()['name'] == "Test User"

# ... other tests ...

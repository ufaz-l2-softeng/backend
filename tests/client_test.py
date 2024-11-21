from fastapi.testclient import TestClient

from src.app.user.manager import user_manager
from src.main import app
from src.app.user.crypto import create_access_token

client = TestClient(app)

# USER #

MOCK_USER = {
    "username": "test_mock_user",
    "password": "secure_password"
}

def test_register_success():
    """Test user registration."""
    response = client.post("/register", json=MOCK_USER)
    print(response)
    assert response.status_code == 200, "User registration failed"
    assert response.json() == ["Successfully registered", 201]


def test_register_duplicate_user():
    """Test duplicate user registration."""
    response = client.post("/register", json=MOCK_USER)
    assert response.status_code == 400, "Duplicate user registration did not fail"
    assert response.json()["detail"] == "Username already exists"


def test_login_success():
    """Test successful login."""
    response = client.post("/login", data=MOCK_USER)
    assert response.status_code == 200, "Login failed"
    assert "access_token" in response.json(), "Access token not returned"


def test_login_invalid_user():
    """Test login with invalid username."""
    response = client.post("/login", data={
        "username": "nonexistent_user",
        "password": "random_password"
    })
    assert response.status_code == 401, "Login with invalid user did not fail"
    assert response.json()["detail"] == "User with username nonexistent_user does not exist"


def test_login_invalid_password():
    """Test login with invalid password."""
    response = client.post("/login", data={
        "username": MOCK_USER["username"],
        "password": "wrong_password"
    })
    assert response.status_code == 401, "Login with invalid password did not fail"
    assert response.json()["detail"] == "Wrong password"


def test_get_me():
    """Test /me endpoint."""
    token = create_access_token(MOCK_USER["username"])
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/me", headers=headers)
    assert response.status_code == 200, "Failed to fetch current user"
    assert response.json()["username"] == MOCK_USER["username"], "Fetched user mismatch"

    user_manager.delete(user_manager.get_user(MOCK_USER["username"]).id)
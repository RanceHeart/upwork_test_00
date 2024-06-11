def test_signup(test_client):
    response = test_client.post("/auth/signup", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_login(test_client):
    response = test_client.post("/auth/login", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200, response.text  # Print the response text if the status is not 200
    assert "access_token" in response.json()

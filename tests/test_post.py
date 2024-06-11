def test_create_post(test_client):
    # signup first
    test_client.post("/auth/signup", json={"email": "test@example.com", "password": "testpassword"})

    login_response = test_client.post("/auth/login", json={"email": "test@example.com", "password": "testpassword"})
    assert login_response.status_code == 200, login_response.text  # Print the response text if the status is not 200
    token = login_response.json().get("access_token")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    response = test_client.post("/posts/addpost", json={"text": "This is a test post"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["text"] == "This is a test post"


def test_get_posts(test_client):
    # signup first
    test_client.post("/auth/signup", json={"email": "test@example.com", "password": "testpassword"})

    login_response = test_client.post("/auth/login", json={"email": "test@example.com", "password": "testpassword"})
    assert login_response.status_code == 200, login_response.text  # Print the response text if the status is not 200
    token = login_response.json().get("access_token")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    response = test_client.get("/posts/getposts", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_delete_post(test_client):
    # signup first
    test_client.post("/auth/signup", json={"email": "test@example.com", "password": "testpassword"})

    login_response = test_client.post("/auth/login", json={"email": "test@example.com", "password": "testpassword"})
    assert login_response.status_code == 200, login_response.text  # Print the response text if the status is not 200
    token = login_response.json().get("access_token")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # Create a post to delete
    create_response = test_client.post("/posts/addpost", json={"text": "This is a test post to delete"},
                                       headers=headers)
    assert create_response.status_code == 200
    post_id = create_response.json()["id"]

    # Delete the post
    delete_response = test_client.delete(f"/posts/deletepost/{post_id}", headers=headers)
    assert delete_response.status_code == 200

    # Verify the post is deleted
    get_response = test_client.get("/posts/getposts", headers=headers)
    posts = get_response.json()
    assert all(post["id"] != post_id for post in posts)

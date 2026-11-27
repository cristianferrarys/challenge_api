async def test_register_user(client):

    response = await client.post(
        "/users",
        json={
            "name": "useruser",
            "email": "test@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data


async def test_register_user(client):

    user_data = await client.post(
        "/users",
        json={
            "name": "useruser",
            "email": "test@example.com",
            "password": "Password123!",
        },
    )

    assert user_data.status_code == 201
    data = user_data.json()

    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data


async def test_login(client):
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


    response = await client.post(
        "/auth/token",
        data={
            "username": data["email"],
            "password": "Password123!",
        },
    )

    assert response.status_code == 200, response.text
    assert response.json()["access_token"] is not None


async def test_login_inválidas(client):
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


    response = await client.post(
        "/auth/token",
        data={
            "username": data["email"],
            "password": "Passwor3!",
        },
    )

    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Credenciales inválidas"}

async def test_create_user_email_duplicado(client):
    user1 = {
        "name": "useruser",
        "email": "test@example.com",
        "password": "Password123!",
    }
    response = await client.post(
        "/users",
        json=user1,
    )
    assert response.status_code == 201
    response2 = await client.post(
        "/users",
        json=user1,
    )
    assert response2.status_code == 409, response2.text
    assert response2.json() == {"detail":"El email ya está registrado"}

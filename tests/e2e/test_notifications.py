
async def authenticate(client):

    user = {
        "name": "useruser",
        "email": "test@example.com",
        "password": "hola123",
    }
    # Registrar usuario
    response = await client.post("/users", json=user)

    assert response.status_code == 201, response.text

    # Autenticar usuario
    response = await client.post(
        "/auth/token",
        data={
            "name": user["name"],
            "username": user["email"],
            "password": user["password"],
        },
    )

    assert response.status_code == 200, response.text

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


async def test_create_notification(client):

    headers = await authenticate(client)

    response = await client.post(
        "/notifications",
        headers=headers,
        json={
            "titulo": "Notificación de prueba",
            "contenido": "Mensaje de prueba",
            "canal": "email",
            "destinatario": "test@example.com",
        },
    )

    assert response.status_code == 201, response.text
    assert response.json()["canal"] == "email"


async def test_get_notifications(client):

    headers = await authenticate(client)
    print("header ", headers)
    response = await client.get(
        "/notifications",
        headers=headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_notifications_without_token(client):

    response = await client.get("/notifications")

    assert response.status_code == 401

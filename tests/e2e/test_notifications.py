from uuid import uuid4

from app.models.notification import Notification
from app.repositories.noti_repository_impl import (
    NotiRepositoryImpl,
)


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
    response = await client.get(
        "/notifications",
        headers=headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_notifications_without_token(client):

    response = await client.get("/notifications")

    assert response.status_code == 401


"""test con mock db template """
async def test_get_notification_mock(client, mocker):
    """"login """
    headers = await authenticate(client)
    """"login """
    notification_id = uuid4()

    notification = Notification(
        id=notification_id,
        titulo="Notificación simulada",
        contenido="Contenido simulado",
        canal="email",
        destinatario="test@example.com",
    )

    spy = mocker.patch.object(
        NotiRepositoryImpl,
        "find_by_id_and_user_id",
        return_value=notification,
    )

    response = await client.get(
        f"/notifications/{notification_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(notification_id)
    assert response.json()["titulo"] == "Notificación simulada"

    spy.assert_awaited_once()


async def test_notification_not_found(client, mocker):

    headers = await authenticate(client)
    notification_id = uuid4()

    # Mock de la respuesta del repositorio
    spy = mocker.patch.object(
        NotiRepositoryImpl,
        "find_by_id_and_user_id",
        return_value=None,
    )

    # Ejecutar endpoint
    response = await client.get(
        f"/notifications/{notification_id}",
        headers=headers,
    )
    # Validar respuesta HTTP
    assert response.status_code == 404
    # Validar llamada al repositorio
    spy.assert_awaited_once()

"""test con mock db template """

async def test_notification_update_ok(client, mocker):

    headers = await authenticate(client)
    notification_id = uuid4()
    notification = Notification(
        id=notification_id,
        titulo="Notificación simulada",
        contenido="Contenido simulado",
        canal="email",
        destinatario="test@example.com",
    )
    # Mock de la respuesta del repositorio
    spy = mocker.patch.object(
        NotiRepositoryImpl,
        "save",
        return_value=None,
    )

    # Ejecutar endpoint
    response = await client.get(
        f"/notifications/{notification_id}",
        headers=headers,
    )
    # Validar respuesta HTTP
    assert response.status_code == 404
    # Validar llamada al repositorio
    spy.assert_awaited_once()
import pytest

from app.strategies.email_strategy import EmailStrategy
from app.strategies.sms_strategy import SMSStrategy
from app.strategies.push_strategy import PushStrategy
from tests.e2e.test_notifications import authenticate

async def test_email_strategy(client, mocker):

    headers = await authenticate(client)

    spy = mocker.spy(EmailStrategy, "send")

    payload = {
        "titulo": "Bienvenido",
        "contenido": "Registro exitoso",
        "canal": "email",
        "destinatario": "test@example.com",
    }

    response = await client.post(
        "/notifications",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["canal"] == "email"
    assert data["destinatario"] == payload["destinatario"]

    spy.assert_awaited_once()

    # Verificar persistencia en PostgreSQL
    response = await client.get(
        f"/notifications/{data['id']}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json() == data
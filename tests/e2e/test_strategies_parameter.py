
import pytest

from app.strategies.email_strategy import EmailStrategy
from app.strategies.sms_strategy import SMSStrategy
from app.strategies.push_strategy import PushStrategy
from tests.e2e.test_notifications import authenticate

@pytest.mark.parametrize(
    "canal, destinatario, strategy",
    [
        (
            "email",
            "test@example.com",
            EmailStrategy,
        ),
        (
            "sms",
            "+5493875123456",
            SMSStrategy,
        ),
        (
            "push",
            "device_token_12345678901234567890",
            PushStrategy,
        ),
    ],
    ids=["email", "sms", "push"],
)
async def test_notification_strategy(
    client,
    mocker,
    canal,
    destinatario,
    strategy,
):

    headers = await authenticate(client)

    spy = mocker.spy(strategy, "send")

    payload = {
        "titulo": "Test notification",
        "contenido": "Mensaje de prueba",
        "canal": canal,
        "destinatario": destinatario,
    }

    response = await client.post(
        "/notifications",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["canal"] == canal
    assert data["destinatario"] == destinatario
    assert data["titulo"] == payload["titulo"]
    assert data["contenido"] == payload["contenido"]

    spy.assert_awaited_once()

    # Verificar persistencia
    response = await client.get(
        f"/notifications/{data['id']}",
        headers = headers,
    )

    assert response.status_code == 200
    assert response.json() == data

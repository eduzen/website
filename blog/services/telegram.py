from typing import Any

import requests
from django.conf import settings

BASE_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}"


def send_message(message: str) -> dict[str, Any]:
    endpoint = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": settings.TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(endpoint, data=payload)
    response.raise_for_status()
    return response.json()


def send_contact_message(name: str, email: str, message: str) -> dict:
    # Here, you can format the message or handle additional logic if needed
    formatted_message = f"Message from website: Name: {name}, Email: {email}, Message: {message}"
    return send_message(formatted_message)

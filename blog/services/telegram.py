from typing import Any

import requests
from django.conf import settings

BASE_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}"


def send_message(text: str) -> dict[str, Any]:
    endpoint = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": settings.TELEGRAM_CHAT_ID, "text": text}
    response = requests.post(endpoint, data=payload)
    response.raise_for_status()
    return response.json()

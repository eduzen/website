import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN  # type: ignore
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID  # type: ignore

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Placeholder tokens used when Telegram is not configured (e.g. tests, CI)
_PLACEHOLDER_TOKENS = {"", "foo", "changeme"}

REQUEST_TIMEOUT_SECONDS = 10


def send_message(message: str) -> dict[str, str]:
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN in _PLACEHOLDER_TOKENS:
        logger.warning("Telegram not configured (token=%r), skipping message", TELEGRAM_TOKEN)
        return {"ok": "true", "description": "skipped — Telegram not configured"}

    endpoint = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(endpoint, data=payload, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


def send_contact_message(name: str, email: str, message: str) -> dict:
    formatted_message = f"Message from website: Name: {name}, Email: {email}, Message: {message}"
    return send_message(formatted_message)

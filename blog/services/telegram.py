import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN  # type: ignore
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID  # type: ignore

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Placeholder tokens used when Telegram is not configured (e.g. tests, CI)
_PLACEHOLDER_TOKENS = {"", "foo", "changeme", "somekey"}

REQUEST_TIMEOUT_SECONDS = 10


def _has_valid_telegram_token(token: str) -> bool:
    return bool(token and token not in _PLACEHOLDER_TOKENS and ":" in token)


def send_message(message: str) -> dict[str, object] | None:
    if not _has_valid_telegram_token(TELEGRAM_TOKEN):
        logger.warning("Telegram not configured (token=%r), skipping message", TELEGRAM_TOKEN)
        return None

    endpoint = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(endpoint, data=payload, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()

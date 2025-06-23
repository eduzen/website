import requests
from django.conf import settings

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN  # type: ignore
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID  # type: ignore

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def send_message(message: str) -> dict[str, str]:
    endpoint = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(endpoint, data=payload)
    response.raise_for_status()
    return response.json()


def send_contact_message(name: str, email: str, message: str) -> dict:
    # Here, you can format the message or handle additional logic if needed
    formatted_message = f"Message from website: Name: {name}, Email: {email}, Message: {message}"
    return send_message(formatted_message)

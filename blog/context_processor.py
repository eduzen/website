from django.http import HttpRequest


def global_urls(request: HttpRequest) -> dict[str, dict[str, str]]:
    urls = {
        "linkedin": "https://www.linkedin.com/in/eduzen/",
        "github": "https://github.com/eduzen",
        "email": "mailto:me@eduzen.com.ar",
        "telegram": "https://t.me/eduzen",
    }
    return {"global_urls": urls}

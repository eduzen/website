import datetime as dt

from django.http import HttpRequest


def global_data(request: HttpRequest) -> dict[str, dict[str, str]]:
    start_year = 2011
    start_python = 2014
    current_year = dt.datetime.now().year
    data = {
        "linkedin": "https://www.linkedin.com/in/eduzen/",
        "github": "https://github.com/eduzen",
        "email": "mailto:me@eduzen.com.ar",
        "telegram": "https://t.me/eduzen",
        "years_in_python": current_year - start_python,
        "years_of_experience": current_year - start_year,
    }
    return {"global_data": data}

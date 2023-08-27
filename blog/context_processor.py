import datetime as dt

from django.http import HttpRequest


def global_data(request: HttpRequest) -> dict[str, dict[str, str]]:
    start_year = 2011
    start_python = 2014
    current_year = dt.datetime.now().year
    python_years = current_year - start_python
    dev_years = current_year - start_year
    data = {
        "linkedin": "https://www.linkedin.com/in/eduzen/",
        "github": "https://github.com/eduzen",
        "email": "mailto:me@eduzen.com.ar",
        "telegram": "https://t.me/eduzen",
        "years_in_python": str(python_years),
        "years_of_experience": str(dev_years),
    }
    return {"global_data": data}

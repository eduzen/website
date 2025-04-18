import datetime as dt

from django.http import HttpRequest

# Constants representing the starting years for development and Python experience.
START_DEVELOPMENT_YEAR = 2011
START_PYTHON_YEAR = 2014


def global_data(request: HttpRequest) -> dict[str, dict[str, str]]:
    """
    A Django context processor that injects global context data into every template.

    This includes:
    - Social and contact links (LinkedIn, GitHub, email, Telegram)
    - Years of Python experience
    - Total years of development experience

    Args:
        request (HttpRequest): The incoming request object. Unused directly,
        but required by the context processor signature.

    Returns:
        dict[str, dict[str, str]]: A dictionary with a single key "global_data",
        whose value is a dictionary containing various global values accessible in templates.
    """
    current_year = dt.datetime.now().year
    python_experience = current_year - START_PYTHON_YEAR
    total_experience = current_year - START_DEVELOPMENT_YEAR

    data = {
        "linkedin": "https://www.linkedin.com/in/eduzen/",
        "github": "https://github.com/eduzen",
        "email": "mailto:me@eduzen.com.ar",
        "telegram": "https://t.me/eduzen",
        "years_in_python": str(python_experience),
        "years_of_experience": str(total_experience),
    }
    return {"global_data": data}

import datetime as dt

from django.http import HttpRequest

# Constants representing the starting years for development and Python experience.
START_DEVELOPMENT_YEAR = 2011
START_PYTHON_YEAR = 2014
BIRTH_YEAR_MONTH = (1982, 11)  # November 1982
MOVED_TO_NL_YEAR_MONTH = (2020, 6)  # June 2020

_STATIC_GLOBAL_DATA: dict[str, str] = {
    "linkedin": "https://www.linkedin.com/in/eduzen/",
    "github": "https://github.com/eduzen",
    "email": "mailto:me@eduzen.com.ar",
    "telegram": "https://t.me/eduzen",
}


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
    today = dt.date.today()

    def years_since(year: int, month: int = 1) -> str:
        """Years elapsed, accounting for whether the anniversary month has passed."""
        return str(today.year - year - (1 if today.month < month else 0))

    data = {
        **_STATIC_GLOBAL_DATA,
        "years_in_python": str(today.year - START_PYTHON_YEAR),
        "years_of_experience": str(today.year - START_DEVELOPMENT_YEAR),
        "age": years_since(*BIRTH_YEAR_MONTH),
        "years_in_nl": years_since(*MOVED_TO_NL_YEAR_MONTH),
    }
    return {"global_data": data}

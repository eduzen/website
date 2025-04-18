import datetime as dt

import pytest
from django.test import RequestFactory

from core.context_processor import (
    START_DEVELOPMENT_YEAR,
    START_PYTHON_YEAR,
    global_data,
)


@pytest.mark.django_db
def test_global_data_context_processor():
    # Arrange
    factory = RequestFactory()
    request = factory.get("/")

    # Act
    context = global_data(request)
    global_info = context["global_data"]

    # Assert keys existence
    expected_keys = {
        "linkedin",
        "github",
        "email",
        "telegram",
        "years_in_python",
        "years_of_experience",
    }
    assert expected_keys.issubset(global_info.keys())

    # Check that years are computed correctly
    current_year = dt.datetime.now().year
    expected_python_years = str(current_year - START_PYTHON_YEAR)
    expected_dev_years = str(current_year - START_DEVELOPMENT_YEAR)

    assert global_info["years_in_python"] == expected_python_years
    assert global_info["years_of_experience"] == expected_dev_years
    assert global_info["linkedin"] == "https://www.linkedin.com/in/eduzen/"
    assert global_info["github"] == "https://github.com/eduzen"
    assert global_info["email"] == "mailto:me@eduzen.com.ar"
    assert global_info["telegram"] == "https://t.me/eduzen"

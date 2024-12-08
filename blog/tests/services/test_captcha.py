import pytest

from blog.services.captcha import verify_captcha


@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("red", True),
        ("RED", True),
        (" rEd ", True),
        ("rojo", True),
        ("ROJO", True),
        ("  rojo  ", True),
        ("blue", False),
        ("", False),
        (" ", False),
        (None, False),  # If you allow None in your code, handle it before calling verify_captcha
    ],
)
def test_verify_captcha(input_value, expected):
    # Since verify_captcha expects a string, ensure input_value is a string or handle None
    # For this test, if input_value is None, pass an empty string to the function.
    user_answer = input_value if isinstance(input_value, str) else ""
    result = verify_captcha(user_answer)
    assert result == expected

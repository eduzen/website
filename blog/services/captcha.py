def verify_captcha(user_answer: str) -> bool:
    """
    Verify the correctness of a given captcha answer.

    The captcha asks the user what color a red rabbit is. Valid answers
    include 'rojo' (Spanish for red) and 'red' (English).

    Args:
        user_answer (str): The user's submitted answer to the captcha question.

    Returns:
        bool: True if the answer is correct (matches 'rojo' or 'red', case-insensitive),
              False otherwise.
    """
    correct_answer = ("rojo", "red")
    if user_answer and user_answer.strip().lower() in correct_answer:
        return True
    return False

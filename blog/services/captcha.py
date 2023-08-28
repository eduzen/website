def verify_captcha(user_answer: str) -> bool:
    correct_answer = ("rojo", "red")
    if user_answer and user_answer.strip().lower() in correct_answer:
        return True
    return False

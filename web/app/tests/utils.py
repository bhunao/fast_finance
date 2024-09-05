
import random
import string


def get_random_int() -> int:
    return random.randint(0, 100)


def get_random_string() -> str:
    return "".join(random.choices(string.ascii_letters, k=32))

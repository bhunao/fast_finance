"""Testing app.core.security functions related to security and password hashing."""
from datetime import timedelta

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.tests.utils import get_random_int, get_random_string


def test_acess_token():
    test_id = get_random_int()
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = create_access_token(test_id, access_token_expires)
    assert token


def test_hashing_algorithm():
    password = get_random_string()
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password)

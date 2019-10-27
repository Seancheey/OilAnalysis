from BackEnd.tableddl import *
from BackEnd.errors import *
from BackEnd.objects import *


def register(username: str, password_sha256: str, email: str):
    """
    new account registration.
    Should raise different errors if username/email already exists.

    :param username: required
    :param password_sha256: required, SHA2-256 of the password
    :param email: required
    """
    pass


def login(username: str, password_sha256: str) -> str:
    """
    make an existing user login. Return a new session id which has an expiration date.
    Should raise errors when user not exists or username and password doesn't match

    :param username: required
    :param password_sha256: required
    :return: session token for user which user should carry around for logged-in operations
    """
    pass


def comment(session_token: str, news_id: int, message: str):
    """
    logged-in user comment on certain news
    Should check token expiration and raise error if it does.

    :param session_token: required
    :param news_id: required
    :param message: required
    """
    pass


def get_oil_prices(start_time: int, end_time: int, oil_type: int) -> list:
    """
    get oil price within certain range (not required) for certain type

    :param start_time: optional
    :param end_time: optional
    :param oil_type: required
    :return: list of oil price objects
    """
    pass


def get_oil_news(start_time: int, end_time: int) -> list:
    """
    get oil news within certain range of time. (not required)

    :param start_time: optional
    :param end_time: optional
    :return: list of oil news objects
    """
    pass

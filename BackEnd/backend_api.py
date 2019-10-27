from BackEnd.tableddl import *
from BackEnd.errors import *


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


def comment(session_token: str, ):
    """

    :param session_token:
    :return:
    """
    pass


def get_oil_prices(session_token: str, start_time: int, end_time: int, oil_type: int) -> list:
    pass


def get_oil_news(session_token: str, start_time: int, end_time: int) -> list:
    pass

from datetime import datetime, timedelta
from random import choices
from string import ascii_letters

from BackEnd.api.utils import new_session, get_login_session
from BackEnd.errors import UserAlreadyExistsError, EmailAlreadyExistsError, UserPasswordNoMatchError, \
    UsernameDoNotExistsError, EmailDoNotExistsError
from BackEnd.objects import User, LoginSession


def register(username: str, password_sha256: bytes, email: str):
    """
    new account registration.
    Should raise different errors if username/email already exists.

    :param username: required
    :param password_sha256: required, SHA3-256 of the password
    :param email: required
    """
    with new_session() as session:
        for _ in session.query(User).filter(User.username == username):
            raise UserAlreadyExistsError()
        for _ in session.query(User).filter(User.email == email):
            raise EmailAlreadyExistsError()
        user = User(username=username, email=email, password=password_sha256)
        session.add(user)
        session.commit()


def login(username_or_email: str, password_sha256: bytes, expire_day_len: int = 30) -> str:
    """
    make an existing user login. Return a new session id which has an expiration date.
    Should raise errors when user not exists or username and password doesn't match

    :param username_or_email: required
    :param password_sha256: required
    :param expire_day_len: optional, days before returned login token expires
    :return: session token for user which user should carry around for logged-in operations
    """
    with new_session() as session:
        result = session.query(User)
        # figure out if input is username or email
        col_to_match = User.email if ('@' in username_or_email and '.' in username_or_email) else User.username
        result = result.filter(col_to_match == username_or_email, User.password == password_sha256)
        user = result.one_or_none()
        if user:
            # generate session token
            raw = ''.join(choices(ascii_letters, k=LoginSession.session_token.property.columns[0].type.length))
            exp_date = datetime.now() + timedelta(days=expire_day_len)
            session.add(LoginSession(session_token=raw, username=user.username, expiration_time=exp_date))
            session.commit()
            return raw
        else:
            # when query returns 0 users, see if user password is incorrect or user doesn't exists
            for _ in session.query(User).filter(col_to_match == username_or_email):
                raise UserPasswordNoMatchError()
            raise EmailDoNotExistsError if col_to_match is User.email else UsernameDoNotExistsError


def logout(session_token: str):
    """
    logout user. Even if session is not found, no errors will be raised.
    :param session_token: required
    """
    with new_session() as session:
        session.query(LoginSession).filter(LoginSession.session_token == session_token).delete()


def get_session_username(session_token: str) -> str:
    """
    :param session_token: required
    :return: username for that session provided
    """
    with new_session() as session:
        login_session = get_login_session(session, session_token)
        return login_session.username

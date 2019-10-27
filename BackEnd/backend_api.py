from BackEnd.tableddl import *
from BackEnd.errors import *
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from random import choices
from string import ascii_letters
from contextlib import contextmanager

__Session = sessionmaker()
__Session.configure(bind=engine)


@contextmanager
def new_session():
    """Provide a transactional scope around a series of operations."""
    session = __Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def register(username: str, password_sha256: bytes, email: str):
    """
    >>> register("user",b'abcdabcdabcdabcdabcdabcdabcdabcd', "adls371@outlook.com")

    new account registration.
    Should raise different errors if username/email already exists.

    :param username: required
    :param password_sha256: required, SHA2-256 of the password
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


def login(username: str, password_sha256: bytes, expire_day_len: int = 30) -> str:
    """
    >>> import random
    >>> random.seed(0)
    >>> login("user", b'abcdabcdabcdabcdabcdabcdabcdabcd')
    'RNvnAvOpyEVAoNGn'

    make an existing user login. Return a new session id which has an expiration date.
    Should raise errors when user not exists or username and password doesn't match

    :param username: required
    :param password_sha256: required
    :param expire_day_len: optional, days before returned login token expires
    :return: session token for user which user should carry around for logged-in operations
    """
    with new_session() as session:
        result = session.query(User).filter(User.username == username, User.password == password_sha256)
        if result.count() == 0:
            for _ in session.query(User).filter(User.username == username):
                raise UserPasswordNoMatchError()
            raise UserDoNotExistsError()
        else:
            for user in result:
                # generate session
                raw = ''.join(choices(ascii_letters, k=LoginSession.session_token.property.columns[0].type.length))
                exp_date = datetime.now() + timedelta(days=expire_day_len)
                session.add(LoginSession(session_token=raw, username=user.username, expiration_time=exp_date))
                session.commit()
                return raw
        assert False


def comment(session_token: str, news_id: int, message: str):
    """
    >>> comment('RNvnAvOpyEVAoNGn', 1, 'test message')

    logged-in user comment on certain news
    Should check token expiration and raise error if it does.

    :param session_token: required
    :param news_id: required
    :param message: required
    """
    with new_session() as session:
        result = session.query(LoginSession).filter(LoginSession.session_token == session_token)
        if result.count == 0:
            raise LoginSessionExpired()
        else:
            for login_session in result:
                session.add(Comment(news_id=news_id, username=login_session.username, text=message))
                session.commit()
                return
        assert False


def get_oil_prices(oil_index: int, start_time: datetime = None, end_time: datetime = None) -> list:
    """
    get oil price within certain range (not required) for certain type

    :param oil_index: id of certain index name for oil, required
    :param start_time: optional
    :param end_time: optional
    :return: list of oil price objects
    """
    with new_session() as session:
        result = session.query(OilPrice).filter(OilPrice.index_id == oil_index)
        if start_time:
            result = result.filter(OilPrice.price_time > start_time)
        if end_time:
            result = result.filter(OilPrice.price_time < end_time)
        return [price for price in result]


def get_oil_news(start_time: datetime = None, end_time: datetime = None) -> list:
    """
    get oil news within certain range of time. (not required)

    :param start_time: optional
    :param end_time: optional
    :return: list of oil news objects
    """
    with new_session() as session:
        result = session.query(OilNews)
        if start_time:
            result = result.filter(OilNews.publish_date > start_time)
        if end_time:
            result = result.filter(OilNews.publish_date < end_time)
        return [news for news in result]

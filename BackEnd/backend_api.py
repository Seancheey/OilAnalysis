from BackEnd.errors import *
from BackEnd.objects import *
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
    >>> with new_session() as s:
    >>>     s.delete(User).filter_by(username='test_user')
    >>> register("test_user",b'abcdabcdabcdabcdabcdabcdabcdabcd', "adls371@outlook.com")

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
        return True


def login(username_or_email: str, password_sha256: bytes, expire_day_len: int = 30) -> str:
    """
    >>> with new_session() as s:
    >>>     s.delete(LoginSession).filter_by(username='test_user')
    >>> import random
    >>> random.seed(0)
    >>> login("test_user", b'abcdabcdabcdabcdabcdabcdabcdabcd')
    'RNvnAvOpyEVAoNGn'

    make an existing user login. Return a new session id which has an expiration date.
    Should raise errors when user not exists or username and password doesn't match

    :param username_or_email: required
    :param password_sha256: required
    :param expire_day_len: optional, days before returned login token expires
    :return: session token for user which user should carry around for logged-in operations
    """
    with new_session() as session:
        result = session.query(User)
        # automatically figure out if input is username or email
        if '@' in username_or_email:
            result = result.filter(User.email == username_or_email, User.password == password_sha256)
        else:
            result = result.filter(User.username == username_or_email, User.password == password_sha256)
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
            for _ in session.query(User).filter(User.username == username_or_email):
                raise UserPasswordNoMatchError()
            raise UserDoNotExistsError()


def get_session_username(session_token: str) -> str:
    """
    >>> get_session_username('RNvnAvOpyEVAoNGn')
    'user'

    :param session_token: required
    :return: username for that session provided
    """
    with new_session() as session:
        token = session.query(LoginSession).filter(LoginSession.session_token == session_token).one_or_none()
        if token:
            if token.expiration_time > datetime.now():
                session.delete(token)
                raise LoginSessionExpired()
            return token.username
        else:
            raise LoginSessionExpired()


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
        login_session = session.query(LoginSession).filter(LoginSession.session_token == session_token).one_or_none()
        if login_session:
            if login_session.expiration_time > datetime.now():
                session.delete(login_session)
            else:
                session.add(Comment(news_id=news_id, username=login_session.username, text=message))
                session.commit()
        else:
            raise LoginSessionExpired()


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
        return [OilPrice(id=price.id, index_id=price.index_id, price=price.price, price_time=price.price_time) for price
                in result]


def get_oil_news(start_time: datetime = None, end_time: datetime = None, news_num: int = -1) -> list:
    """
    >>> get_oil_news(start_time=datetime(year=2018,month=9,day=20)) is not None
    True

    get oil news within certain range of time. (not required)

    :param start_time: optional
    :param end_time: optional
    :param news_num: required, number of news to grab each time, anything < 0 means grab all
    :return: list of oil news objects
    """
    with new_session() as session:
        result = session.query(OilNews).order_by(OilNews.publish_date)
        if start_time:
            result = result.filter(OilNews.publish_date > start_time)
        if end_time:
            result = result.filter(OilNews.publish_date < end_time)
        return [OilNews(id=news.id, title=news.title, publish_date=news.publish_date, author=news.author,
                        content=news.content, reference=news.reference, retrieve_time=news.retrieve_time) for news in
                result]

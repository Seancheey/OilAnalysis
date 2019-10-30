from BackEnd.errors import *
from BackEnd.objects import *
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from random import choices
from string import ascii_letters
from contextlib import contextmanager
import pandas as pd

__Session = sessionmaker()
__Session.configure(bind=engine)


@contextmanager
def new_session() -> Session:
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
    ...     assert s.query(User).filter(or_(User.username=='test_user', User.email=='test@test.com')).delete() >= 0
    ...     s.commit()
    >>> register("test_user",b'abcdabcdabcdabcdabcdabcdabcdabcd', "test@test.com")

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
    >>> with new_session() as session:
    ...     assert session.query(LoginSession).filter(LoginSession.username=='test_user').delete() >= 0
    >>> assert len(login("test_user", b'abcdabcdabcdabcdabcdabcdabcdabcd')) > 0

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


def logout(session_token: str):
    """
    >>> token = login("test_user",b'abcdabcdabcdabcdabcdabcdabcdabcd')
    >>> logout(token)
    >>> with new_session() as session:
    ...     assert session.query(LoginSession).filter(LoginSession.session_token==token).count() == 0

    logout user. Even if session is not found, no errors will be raised.
    :param session_token: required
    """
    with new_session() as session:
        session.query(LoginSession).filter(LoginSession.session_token == session_token).delete()


def __get_login_session(sql_session: Session, session_token: str):
    """
    >>> token = login('test_user', b'abcdabcdabcdabcdabcdabcdabcdabcd', expire_day_len=0)
    >>> try:
    ...     get_session_username(token)
    ...     assert False, "login is supposed to expire"
    ... except LoginSessionExpired:
    ...     pass


    helper function to raise Expire Error when token expired.
    The function also delete the expired key.

    :param sql_session: required. SQLAlchemy session
    :param session_token: login token string
    :return a login session object
    """
    token = sql_session.query(LoginSession).filter(LoginSession.session_token == session_token).one_or_none()
    if token is None:
        raise LoginSessionExpired()
    if token.expiration_time < datetime.now():
        sql_session.delete(token)
        sql_session.commit()
        raise LoginSessionExpired()
    return LoginSession(session_token=token.session_token, username=token.username,
                        expiration_time=token.expiration_time)


def get_session_username(session_token: str) -> str:
    """
    >>> token = login('test_user', b'abcdabcdabcdabcdabcdabcdabcdabcd')
    >>> get_session_username(token)
    'test_user'

    :param session_token: required
    :return: username for that session provided
    """
    with new_session() as session:
        login_session = __get_login_session(session, session_token)
        return login_session.username


def comment(session_token: str, news_id: int, message: str):
    """
    >>> token = login('test_user', b'abcdabcdabcdabcdabcdabcdabcdabcd')
    >>> comment(token, 1, 'test message')

    logged-in user comment on certain news
    Should check token expiration and raise error if it does.

    :param session_token: required
    :param news_id: required
    :param message: required
    """
    with new_session() as session:
        login_session = __get_login_session(session, session_token)
        session.add(Comment(news_id=news_id, username=login_session.username, text=message))
        session.commit()

def pd_get_oil_prices(oil_index: int, start_time: datetime = None, end_time: datetime = None):
    """
    get oil price within certain range (not required) and return as a pandas dataframe

    :param oil_index: id of certain index name for oil, required
    :param start_time: optional
    :param end_time: optional
    :return: pandas dataframe
    """
    with new_session() as session:
        df = pd.read_sql(session.query(OilPrice).filter(OilPrice.index_id == oil_index).statement,session.bind)
        if start_time:
            result = result.filter(OilPrice.price_time > start_time)
        if end_time:
            result = result.filter(OilPrice.price_time < end_time)
        return df


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

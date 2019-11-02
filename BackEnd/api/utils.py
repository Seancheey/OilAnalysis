from datetime import datetime

from BackEnd.errors import LoginSessionExpired
from BackEnd.objects import LoginSession
from BackEnd.settings import engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

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


def get_login_session(sql_session: Session, session_token: str):
    """
    >>> token = login('test_user', b'abcdabcdabcdabcdabcdabcdabcdabcd', expire_day_len=-1)
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
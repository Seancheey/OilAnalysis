from BackEnd.api.utils import *


def comment(session_token: str, target_id: int, message: str, comment_type: Comment.__class__):
    """
    logged-in user comment on certain news
    Should check token expiration and raise error if it does.

    :param session_token: required, session token of user
    :param comment_type: required, should be one of following: NewsComment, PriceComment
    :param target_id: required, target id
    :param message: required
    """
    assert comment_type is NewsComment or comment_type is PriceComment
    with new_session() as session:
        login_session = get_login_session(session, session_token)
        session.add(comment_type(target_id=target_id, username=login_session.username, text=message))
        session.commit()


def get_comments_for_news(news_id: int):
    with new_session() as session:
        result = session.query(NewsComment).filter(NewsComment.target_id == news_id).order_by(NewsComment.comment_time)
        return [com.__dict__ for com in result.all()]


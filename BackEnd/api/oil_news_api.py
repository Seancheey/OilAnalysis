from datetime import datetime

from BackEnd.api.utils import new_session
from BackEnd.objects import OilNews


def __wrap_oil_news(news: OilNews) -> OilNews:
    return OilNews(news_id=news.news_id, title=news.title, publish_date=news.publish_date, author=news.author,
                   content=news.content, reference=news.reference, retrieve_time=news.retrieve_time)


def get_oil_news_list(start_time: datetime = None, end_time: datetime = None, news_num: int = -1) -> list:
    """
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
        if news_num > 0:
            result = result.limit(news_num)
        result = result.all()
        return [__wrap_oil_news(news) for news in result]


def get_one_oil_news(news_id: int) -> OilNews:
    """
    fetch a single oil news

    :param news_id: required, id for news
    :return: OilNews object
    """
    with new_session() as session:
        return __wrap_oil_news(session.query(OilNews).filter(OilNews.news_id == news_id).one_or_none())


def get_latest_news() -> OilNews:
    """
    fetch latest news

    :return: OilNews object
    """
    with new_session() as session:
        return __wrap_oil_news(session.query(OilNews).order_by(OilNews.publish_date.desc()).limit(1).one_or_none())

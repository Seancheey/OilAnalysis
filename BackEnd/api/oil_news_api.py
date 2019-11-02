from datetime import datetime

from BackEnd.api.utils import new_session
from BackEnd.objects import OilNews


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
        return [OilNews(news_id=news.news_id, title=news.title, publish_date=news.publish_date, author=news.author,
                        content=news.content, reference=news.reference, retrieve_time=news.retrieve_time) for news in
                result]
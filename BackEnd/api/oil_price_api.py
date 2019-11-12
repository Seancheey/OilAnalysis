from BackEnd.objects import *
from BackEnd.api.utils import new_session
from datetime import datetime
import pandas as pd
from typing import List


def pd_get_oil_prices(oil_index: int, start_time: datetime = None, end_time: datetime = None):
    """
    get oil price within certain range (not required) and return as a pandas dataframe

    :param oil_index: id of certain index name for oil, required
    :param start_time: optional
    :param end_time: optional
    :return: pandas dataframe
    """
    with new_session() as session:
        df = pd.read_sql(session.query(OilPrice).filter(OilPrice.index_id == oil_index).statement, session.bind)
        return df


def get_oil_prices(oil_index: int, start_time: datetime = None, end_time: datetime = None) -> List[OilPrice]:
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
        return [
            OilPrice(price_id=price.price_id, index_id=price.index_id, price=price.price, price_time=price.price_time)
            for price
            in result]


def get_oil_indices() -> List[OilIndexDenormalized]:
    """
    get all de-normalized oil indices
    :return: list of oil indices objects
    """
    with new_session() as session:
        result = session.query(OilIndex, OilCategory).filter(OilIndex.category_id == OilCategory.category_id).order_by(
            OilIndex.index_id)
        return [OilIndexDenormalized(iid=i.index_id, iname=i.index_name, cid=c.category_id, cname=c.category_name) for
                i, c in result]

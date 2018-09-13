# -*- coding: utf-8 -*-
import scrapy
from OilAnalysis.sqlsettings import *
from datetime import datetime, timedelta
from OilAnalysis.runspider import run


class OilDailyPriceSpider(scrapy.Spider):
    name = 'oil_daily_price'
    allowed_domains = ['oilprice.com/oil-price-charts']
    start_urls = ['https://oilprice.com/oil-price-charts/']

    def parse(self, response):
        price_tables = response.css('div.oilprices__centercolumn table')
        for table in price_tables:
            # get index category name
            table_name = table.css('th::text').extract_first()
            body = table.css('tbody.row_holder tr')
            for row in body:
                # get time entry from two sources
                time = row.css('td.last_updated::attr("data-stamp")').extract_first()
                if time == "":
                    time = row.css('td.last_updated::text').extract_first()
                # if time is not get, it's more like a subtitle table row, so skip it
                if not time:
                    continue
                # convert time to iso format
                time = self.convert_time(time)
                # convert string like "+2.0%" to float
                percent_change = row.css('td.change_up_percent::text,td.change_down_percent::text').extract_first()
                percent_change = float(percent_change[:-1])
                # convert string to float
                abs_change = float(row.css('td.change_up::text,td.change_down::text').extract_first())
                last_price = float(row.css('td.last_price::text').extract_first())
                yield {
                    col_price_category: table_name,
                    col_price_index_name: row.css('td::text').extract_first(),
                    col_price_last: last_price,
                    col_price_abs_change: abs_change,
                    col_price_per_change: percent_change,
                    col_price_update_time: time
                }

    def convert_time(self, time) -> str:
        # convert string time to datetime
        cur_year = datetime.now().strftime("%Y")
        finished = False
        if not finished:
            try:
                time = datetime.strptime(time + cur_year, "(%d %B)%Y").isoformat()
                finished = True
            except ValueError:
                pass
        if not finished:
            try:
                time = datetime.strptime(time + cur_year, "(%B. price)%Y").isoformat()
                finished = True
            except ValueError:
                pass
        if not finished:
            try:
                time = datetime.fromtimestamp(int(time)).isoformat()
                finished = True
            except ValueError:
                pass
        if not finished:
            try:
                today = datetime.now()
                delay_day = int(time.split()[0][1:])
                time = (today - timedelta(days=delay_day)).isoformat()
                finished = True
            except ValueError:
                pass
        if not finished:
            raise ValueError("time with string: %s cannot be parsed with current settings." % time)
        return time


if __name__ == "__main__":
    try:
        with open("price_last_update.txt", "r") as f:
            last_time = datetime.strptime(f.readline(), "%Y-%m-%dT%H:%M:%S.%f")
            if (datetime.now() - last_time).days >= 1 or (datetime.now() - last_time).seconds >= 84600:
                run(OilDailyPriceSpider)
            else:
                pass
    except FileNotFoundError:
        run(OilDailyPriceSpider)
    finally:
        with open("price_last_update.txt", "w") as f:
            f.write(datetime.now().isoformat())

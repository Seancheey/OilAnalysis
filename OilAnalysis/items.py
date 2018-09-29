# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import Item
from scrapy.loader.processors import Join, TakeFirst
from datetime import datetime


class NewsItem(Item):
    title = scrapy.Field(output_processor=TakeFirst())
    author = scrapy.Field(output_processor=TakeFirst())
    content = scrapy.Field(input_processor=Join("\n"), output_processor=TakeFirst())
    publish_date = scrapy.Field(
        input_processor=lambda x: datetime.strptime(" ".join(x[1].split()[:-1]), "- %b %d, %Y, %I:%M %p"),
        output_processor=lambda x: x[0].isoformat().replace("T", " ")
    )
    reference = scrapy.Field(output_processor=TakeFirst())


class StockItem(Item):
    volume = scrapy.Field(output_processor=TakeFirst())
    update_time = scrapy.Field(output_processor=TakeFirst())
    stock_name = scrapy.Field(output_processor=TakeFirst())

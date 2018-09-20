# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader, Item
from scrapy.loader.processors import Join, TakeFirst
from scrapy.exceptions import CloseSpider
from OilAnalysis.runspider import run
from datetime import datetime


class News(Item):
    title = scrapy.Field(output_processor=TakeFirst())
    author = scrapy.Field(output_processor=TakeFirst())
    # convert '?' to other
    content = scrapy.Field(input_processor=Join("\n"), output_processor=TakeFirst())
    publish_date = scrapy.Field(
        input_processor=lambda x: datetime.strptime(" ".join(x[1].split()[:-1]), "- %b %d, %Y, %I:%M %p"),
        output_processor=lambda x: x[0].isoformat()
    )
    reference = scrapy.Field(output_processor=TakeFirst())


class OilNewsSpider(scrapy.Spider):
    name = "oilnews"
    allowed_domains = ["oilprice.com"]
    start_urls = ['https://oilprice.com/Latest-Energy-News/World-News/']
    iter_urls = ['https://oilprice.com/Energy/Energy-General',
                 'https://oilprice.com/Energy/Oil-Prices',
                 'https://oilprice.com/Energy/Crude-Oil',
                 'https://oilprice.com/Energy/Heating-Oil',
                 'https://oilprice.com/Energy/Gas-Prices',
                 'https://oilprice.com/Energy/Natural-Gas',
                 'https://oilprice.com/Energy/Coal']
    only_today = False

    def parse(self, response):
        yield from self.parse_page(response)
        for url in OilNewsSpider.iter_urls:
            yield response.follow(url, self.parse_page)

    def parse_page(self, response):
        # get all news in the current page
        for article in response.css('div.categoryArticle'):
            news_url = article.css('a::attr("href")').extract_first()
            yield response.follow(news_url, self.parse_news_content)
        # go to next page
        next_url = response.css('div.pagination a.next::attr("href")').extract_first()
        yield response.follow(next_url, self.parse_page)

    def parse_news_content(self, response):
        loader = ItemLoader(item=News(), response=response)
        loader.add_css("title", "div.singleArticle__content h1::text")
        loader.add_css("author", "div.singleArticle__content span.article_byline a::text")
        loader.add_css("publish_date", "div.singleArticle__content span.article_byline::text")
        loader.add_css("content", "div#news-content p::text, div#article-content p::text")
        loader.add_value("reference", response.url)
        item = loader.load_item()
        if OilNewsSpider.only_today and (datetime.now() - item['publish_date']).days >= 1:
            raise CloseSpider("publish_date exceed limit")
        else:
            yield loader.load_item()


if __name__ == "__main__":
    run(OilNewsSpider)

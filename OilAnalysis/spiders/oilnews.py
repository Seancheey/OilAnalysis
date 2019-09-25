# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from OilAnalysis.runspider import run
from OilAnalysis.items import NewsItem


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
    only_today = True

    def parse(self, response):
        yield from self.parse_page(response)
        for url in OilNewsSpider.iter_urls:
            yield response.follow(url, self.parse_page)

    def parse_page(self, response):
        # get all news in the current page
        for article in response.css('div.categoryArticle'):
            news_url = article.css('a::attr("href")').extract_first()
            meta_data = article.css('p.categoryArticle__meta::text').extract_first().split('|')
            date = meta_data[0]
            author = meta_data[1]
            yield response.follow(news_url, lambda r: self.parse_news_content(r, known_date=date, known_author=author))
        if not OilNewsSpider.only_today:
            # go to next page
            next_url = response.css('div.pagination a.next::attr("href")').extract_first()
            yield response.follow(next_url, self.parse_page)

    def parse_news_content(self, response, known_date=None, known_author=None):
        loader = ItemLoader(item=NewsItem(), response=response)
        loader.add_css("title", "div.singleArticle__content h1::text")
        if known_author:
            loader.add_value("author", known_date)
        else:
            loader.add_css("author", "div.singleArticle__content span.article_byline a::text")
        if known_date:
            loader.add_value("publish_date", known_date)
        else:
            loader.add_css("publish_date", "div.singleArticle__content span.article_byline::text")
        loader.add_css("content",
                       "div#news-content p::text, div#article-content p::text, div#article-content span::text")
        loader.add_value("reference", response.url)
        item = loader.load_item()
        yield item


if __name__ == "__main__":
    run(OilNewsSpider)

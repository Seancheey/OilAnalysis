# -*- coding: utf-8 -*-
import scrapy
from OilAnalysis.runspider import run
from OilAnalysis.tableddl import *
from datetime import datetime


class OilNewsSpider(scrapy.Spider):
    name = "oilnews"
    allowed_domains = ["oilprice.com"]
    start_urls = ['https://oilprice.com/Latest-Energy-News/World-News/']

    def parse(self, response):
        # get all news in the current page
        for article in response.css('div.categoryArticle'):
            news_url = article.css('a::attr("href")').extract_first()
            yield response.follow(news_url, self.parse_news_content)
        # go to next page
        next_url = response.css('div.pagination a.next::attr("href")').extract_first()
        yield response.follow(next_url, self.parse)

    def parse_news_content(self, response):
        news = response.css("div.singleArticle__content")
        title = news.css("h1::text").extract_first()
        author = news.css("span.article_byline a::text").extract_first()
        date = news.css("span.article_byline::text").extract()[1][3:]
        content = "\n".join(response.css('div#news-content p::text').extract())
        # format publish_time to standard datetime before insert
        date_str = " ".join(date.split()[:-1])
        date = datetime.strptime(date_str, "%b %d, %Y, %I:%M %p").date().isoformat()
        # replace ( and ) with space
        content = content.replace("(", " ")
        content = content.replace(")", " ")
        content = content.replace("'", " ")
        yield {
            "title": title,
            "publish_date": date,
            "author": author,
            "content": content
        }


if __name__ == "__main__":
    run(OilNewsSpider)

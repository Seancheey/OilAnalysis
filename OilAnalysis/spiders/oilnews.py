# -*- coding: utf-8 -*-
import scrapy


class OilNewsSpider(scrapy.Spider):
	name = "oilnews"
	allowed_domains = ["oilprice.com"]
	start_urls = ['https://oilprice.com/Latest-Energy-News/World-News/']

	def parse(self, response):
		for article in response.css('div.categoryArticle'):
			news_url = article.css('a::attr("href")').extract_first()
			yield response.follow(news_url, self.parse_news_content)

	def parse_news_content(self, response):
		news = response.css("div.singleArticle__content")
		title = news.css("h1::text").extract_first()
		author = news.css("span.article_byline a::text").extract_first()
		date = news.css("span.article_byline::text").extract()[1][3:]
		content = "\n".join(response.css('div#news-content p::text').extract())
		yield {
			"title": title,
			"date": date,
			"author": author,
			"content": content
		}

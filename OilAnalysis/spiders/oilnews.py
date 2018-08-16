# -*- coding: utf-8 -*-
import scrapy


class OilNewsSpider(scrapy.Spider):
	name = "oilnews"
	allowed_domains = ["oilprice.com/Latest-Energy-News/World-News"]
	start_urls = ['https://oilprice.com/Latest-Energy-News/World-News/']

	def parse(self, response):
		for article in response.css('div.categoryArticle'):
			print(article)
			yield {
				"title": article.css('h2.categoryArticle__title::text').extract_first(),
				"excerpt": article.css("p.categoryArticle__excerpt::text").extract_first()
			}

import scrapy

from scrapy.loader import ItemLoader

from ..items import BsisiItem
from itemloaders.processors import TakeFirst


class BsisiSpider(scrapy.Spider):
	name = 'bsisi'
	start_urls = ['https://www.bsi.si/mediji/']

	def parse(self, response):
		post_links = response.xpath('//td[@class="summary"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[contains(@class, "article-content")]/h1/text()').get()
		description = response.xpath('//div[contains(@class, "article-content")]//text()[normalize-space() and not(ancestor::h1 | ancestor::div[@class="news-date"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="news-date"]/text()').get()
		if date:
			date = date.split('/')[0]

		item = ItemLoader(item=BsisiItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

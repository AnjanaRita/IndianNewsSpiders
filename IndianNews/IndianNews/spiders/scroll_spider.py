import scrapy
import json
import re
import datetime
from ast import literal_eval

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url

from ..items import CorpusItem
from ..utils import *

class wireSpider(CrawlSpider):
	name = "scroll"
	allow_domain=['scroll.in']

	start_urls = [
		"https://scroll.in/category/76/politics/page/"
		]
	number_page = 5
	start_page= 1	

	def parse(self,response):
		all_links = response.xpath('//*[@id="feed"]/div/div[1]/ul/li/link/@href').extract()
		for link in all_links:
			if 'video' not in link:
				yield scrapy.Request(url=link, callback=self.extract_data)
		url = "https://scroll.in/category/76/politics/page/"
		if self.number_page < self.start_page:
			self.start_page += 1
			yield scrapy.Request(url= url+ str(self.start_page), callable =self.parse)
		
		
	
	def get_date(self, response):
		date = response.xpath('.//div/section/header/div/div/time[2]/text()').extract()
		return date
	
	def extract_data(self, response):
		url = get_base_url(response)
		date = self.get_date(response)
		content = get_content(response, path = './/p/text()')
		title = get_title(response, path ='.//header/h1/text()')
		author = get_author(response, path= './/div/aside[1]/address/a/text()')
		tag = get_tag(response, './/div/section/ul/li/a/text()')

		tab = CorpusItem()
		tab['content'] = content
		tab['title'] = title
		tab['author'] = author
		tab['tag'] = tag
		tab['date'] = date
		tab['url'] = url
		yield tab


# -*- coding: utf-8 -*-
import scrapy


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    allowed_domains = ['www.amazon.com']
    start_urls = ['http://www.amazon.com/']

    def parse(self, response):
        pass

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonScrapItem(scrapy.Item):
    # product brand shipping price
    product = scrapy.Field()
    price = scrapy.Field()
    # shipping = scrapy.Field()


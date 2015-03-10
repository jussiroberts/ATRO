# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AtroItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    abstract = scrapy.Field()
    keywords = scrapy.Field()
    journal = scrapy.Field()
    otherinfo = scrapy.Field()
    pass

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyBaiduItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    abstract = scrapy.Field()
    url = scrapy.Field()

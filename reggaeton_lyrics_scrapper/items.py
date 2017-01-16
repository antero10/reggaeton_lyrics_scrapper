# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReggaetonLyricsScrapperItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    lyric = scrapy.Field()
    pass

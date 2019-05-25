# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KugoumusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    song_name = scrapy.Field()
    audio_id = scrapy.Field()
    song = scrapy.Field()
    author_name = scrapy.Field()
    song_path = scrapy.Field()


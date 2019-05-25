# -*- coding: utf-8 -*-

import scrapy


class KugoumusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    song_name = scrapy.Field()
    audio_id = scrapy.Field()
    song = scrapy.Field()
    author_name = scrapy.Field()
    song_path = scrapy.Field()


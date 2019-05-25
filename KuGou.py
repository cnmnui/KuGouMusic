# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import sys
sys.path.append('C:/code/test/KuGouMusic/KuGouMusic')
from KuGouMusic.items import KugoumusicItem
import time
import json
import math
import random
import requests
from fake_useragent import UserAgent
import os


class KugouSpider(scrapy.Spider):
    name = 'KuGou'
    allowed_domains = ['kugou.com']
    item = KugoumusicItem()
    k_num = math.floor(1e16 * random.random())
    search_base_url = "https://songsearch.kugou.com/song_search_v2?"
    k_keyword = '周华健'
    k_pagesize = '5'
    k_time = round(time.time() * 1000)

    # 构造起始url
    k_data = {
        'keyword': k_keyword,                          # (搜索内容)
        'page': '1',                                 # (起始页)
        'pagesize': k_pagesize,                        # (每页数量)
        'userid': '-1',
        'clientver': '',
        'platform': 'WebFilter',
        'tag': 'em',
        'filter': '2',
        'iscorrection': '1',
        'privilege_filter': '0',
        '_': k_time
    }
    k_params = urlencode(k_data)
    search_url = search_base_url + k_params
    start_urls = [search_url]

    def parse(self, response):
        response.body.decode('utf-8')
        base_list = json.loads(response.text)['data']['lists']
        for base_info in base_list:
            # self.item['song_name'] = base_info['SongName'][4: -5]
            file_hash = base_info['FileHash']
            k_Privilege = base_info['Privilege']
            song_base_url = 'https://wwwapi.kugou.com/yy/index.php?'
            data = {
                'r': 'play/getdata',
                'callback': 'jQuery1910%s_%s'.format(self.k_num, self.k_time),
                'hash': file_hash,
                'album_id': '',
                'dfid': '1IV66g2RIgzf0BmQfp3F5Htb',
                'mid': '720896131cec2a6b003057fe8645803b',
                'platid': '4',
                '_': self.k_time
            }
            if k_Privilege != 10:
                song_url = song_base_url + urlencode(data)
                yield scrapy.Request(song_url, callback=self.parse_song_list)

    def parse_song_list(self, response):
        response.body.decode('utf-8')
        song_info = json.loads(response.text[16: -2])
        self.item['song_name'] = song_info['data']['audio_name']
        self.item['audio_id'] = song_info['data']['audio_id']
        song_link = song_info['data']['play_url']
        self.item['author_name'] = song_info['data']['author_name']
        file_path = 'C:/music/' + self.item['author_name'] + '/'
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        self.item['song_path'] = file_path + self.item['song_name'] + '.mp3'
        self.parse_song(song_link)
        yield self.item

    def parse_song(self, song_link):
        ua = UserAgent()
        headers = {"UserAgent": ua.random}
        k_res = requests.get(song_link, headers=headers)
        k_res.encoding = 'utf-8'
        self.item['song'] = k_res.content
        return self.item['song']




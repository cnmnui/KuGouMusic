# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import sys
sys.path.append('你的路径')
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
    path = 'C:/music/'
    k_num = math.floor(1e16 * random.random())
    search_base_url = "https://songsearch.kugou.com/song_search_v2?"
    k_keyword = '周华健'                              # 搜索关键词
    k_pagesize = '5'                                 # 每页加载数量
    k_time = round(time.time() * 1000)               # 时间值

    # 构造起始url
    k_data = {
        'keyword': k_keyword,                          # (搜索内容)
        'page': '1',                                   # (起始页)
        'pagesize': k_pagesize,                        # (每页数量)
        'userid': '-1',                                # 用户ID, 未登录为-1
        'clientver': '',
        'platform': 'WebFilter',
        'tag': 'em',
        'filter': '2',
        'iscorrection': '1',
        'privilege_filter': '0',
        '_': k_time                                     # 时间值
    }
    k_params = urlencode(k_data)
    search_url = search_base_url + k_params
    start_urls = [search_url]

    def parse(self, response):
        """
        对起始页解析
        得到并返回歌曲信息
        """
        response.body.decode('utf-8')
        base_list = json.loads(response.text)['data']['lists']
        for base_info in base_list:
            # self.item['song_name'] = base_info['SongName'][4: -5]
            file_hash = base_info['FileHash']
            k_Privilege = base_info['Privilege']
            song_base_url = 'https://wwwapi.kugou.com/yy/index.php?'
            # 构造请求链接
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
            # 如果Privilege值为10，则为收费歌曲
            if k_Privilege != 10:
                song_url = song_base_url + urlencode(data)
                yield scrapy.Request(song_url, callback=self.parse_song_list)

    def parse_song_list(self, response):
        """
        对歌曲信息页进行解析
        获取到所要抓取的歌曲信息
        """
        response.body.decode('utf-8')
        song_info = json.loads(response.text[16: -2])
        self.item['song_name'] = song_info['data']['audio_name'].split('-')[-1][1:]
        self.item['audio_id'] = song_info['data']['audio_id']
        song_link = song_info['data']['play_url']
        self.item['author_name'] = song_info['data']['author_name']
        # 歌曲的存放路径
        file_path = self.path + self.item['author_name'] + '/'
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        self.item['song_path'] = file_path + self.item['song_name'] + '.mp3'
        self.parse_song(song_link)
        yield self.item

    def parse_song(self, song_link):
        """
        解析歌曲链接
        """
        ua = UserAgent()
        headers = {"UserAgent": ua.random}
        k_res = requests.get(song_link, headers=headers)
        k_res.encoding = 'utf-8'
        self.item['song'] = k_res.content
        return self.item['song']




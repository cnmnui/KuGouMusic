# -*- coding: utf-8 -*-

import pymysql
from twisted.enterprise import adbapi
import sys
sys.path.append('你的路径')
from KuGouMusic import settings


class KuGouMusicPipeline(object):
    # 保存歌曲到本地文件
    def process_item(self, item, spider):
        with open(item['song_path'], 'wb') as f:
                f.write(item['song'])
        self.to_mysql(item)

    # 保存歌曲信息到数据库
    def to_mysql(self, item):
        m_host = settings.MYSQL_HOST
        m_user = settings.MYSQL_USER
        m_psword = settings.MYSQL_PASSWORD
        m_db = settings.MYSQL_DBNAME
        m_table = settings.MYSQL_TABLE
        conn = pymysql.connect(m_host, m_user, m_psword, m_db, charset='utf8mb4')
        cursor = conn.cursor()
        try:
            ins = "insert into {0}.{1}(audio_id,song_name,author_name,song_path) " \
                  "values(%s,%s,%s,%s)" .format(m_db, m_table)
            m_values = (item['audio_id'], item['song_name'], item['author_name'], item['song_path'])
            cursor.execute(ins, m_values)
        except ValueError as e:
            print(e)
            conn.rollback()
        finally:
            conn.commit()
            cursor.close()
            conn.close()
            
            
            
            
        

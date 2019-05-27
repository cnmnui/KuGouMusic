# -*- coding: utf-8 -*-

import pymysql
from twisted.enterprise import adbapi
import sys
sys.path.append('你的路径')
m KuGouMusic.settings import Mysql_Info


# 保存歌曲文件
class KuGouMusicPipeline(object):
    def process_item(self, item, spider):
        with open(item['song_path'], 'wb') as f:
                f.write(item['song'])
        self.to_mysql(item)

    def to_mysql(self, item):
        m_host = Mysql_Info['host']
        m_user = Mysql_Info['user']
        m_psword = Mysql_Info['password']
        m_db = Mysql_Info['database']
        m_table = Mysql_Info['table']
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
            
            
            
        

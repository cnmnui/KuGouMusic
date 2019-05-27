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
            conn.commit()
        except ValueError as e:
            print(e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            
            
# # 保存歌曲文件
# class KuGouMusicPipeline(object):
#     def process_item(self, item, spider):
#         with open(item['song_path'], 'wb') as k_f:
#                 k_f.write(item['song'])


# # 保存到数据库
# class ToMysqlPipeline(object):
#     def __init__(self):
#         m_host = settings.MYSQL_HOST
#         m_user = settings.MYSQL_USER
#         m_psword = settings.MYSQL_PASSWORD
#         self.m_db = settings.MYSQL_DBNAME
#         self.m_table = settings.MYSQL_TABLE
#         self.conn = pymysql.connect(m_host, m_user, m_psword, self.m_db, charset='utf8mb4')
#         self.cursor = self.conn.cursor()

#     def process_item(self, item, spider):
#         ins = "insert into {0}.{1}(audio_id,song_name,author_name,song_path) values(%s,%s,%s,%s)"\
#             .format(self.m_db, self.m_table)
#         m_values = (item['audio_id'], item['song_name'], item['author_name'], item['song_path'])
#         self.cursor.execute(ins, m_values)
#         # massage_s = self.cursor.fetchall()
#         # print(massage_s)
#         self.conn.commit()

#     def close_mysql(self):
#         self.cursor.close()
#         self.conn.close()
            
            
            
            
        

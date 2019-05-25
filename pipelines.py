# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
import sys
sys.path.append('C:/code/test/KuGouMusic/KuGouMusic')
from KuGouMusic import settings


# 保存歌曲文件
class KuGouMusicPipeline(object):
    def process_item(self, item, spider):
        with open(item['song_path'], 'wb') as f:
                f.write(item['song'])
        self.to_mysql(item)

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


# 保存到数据库
# class ToMysqlPipeline(object):
#     def __init__(self):
#         self.conn = pymysql.connect("localhost", "root", "12358", "kugou", charset="utf8mb4")
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         ins = "insert into kugou.music(audio_id,song_name,author_name,song_path) values(%s,%s,%s,%s)"
#         m_values = (item['audio_id'], item['song_name'], item['author_name'], item['song_path'])
#         self.cursor.execute(ins, m_values)
#         self.conn.commit()
#
#     def close_mysql(self):
#         self.cursor.close()
#         self.conn.close()


# 保存歌曲文件
# class KuGouMusicPipeline(object):
#     def process_item(self, item, spider):
#         with open(item['song_path'], 'wb') as k_f:
#                 k_f.write(item['song'])
#
#
# # 异步保存到mysql
# class ToMysqlPipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         """
#         数据库建立连接
#         :param settings: 配置参数
#         :return: 实例化参数
#         """
#         adbparams = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             password=settings['MYSQL_PASSWORD'],
#             charset=settings["MYSQL_CHARSET"],
#             cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
#         )
#         # 连接数据池ConnectionPool，使用pymysql连接
#         dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
#         # 返回实例化参数
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         """
#         使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
#         """
#         k_query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
#         # 添加异常处理
#         k_query.addCallback(self.handle_error)  # 处理异常
#
#     @staticmethod
#     def do_insert(cursor, item):
#         m_ins = "insert into kugou.music(audio_id,song_name,author_name,song_path) values(%s,%s,%s,%s)"
#         m_values = (item['audio_id'], item['song_name'], item['author_name'], item['song_path'])
#         cursor.execute(m_ins, m_values)
#
#     @staticmethod
#     def handle_error(failure):
#         if failure:
#             # 打印错误信息
#             print(failure)


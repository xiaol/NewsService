# coding=utf-8
from datetime import datetime

import psycopg2
from psycopg2 import pool

from settings import *
from utils.utility import get_mongodb

def get_postgredb():
    connection = psycopg2.connect(database=POSTGRE_DBNAME, user=POSTGRE_USER, password=POSTGRE_PWD, host=POSTGRE_HOST,)
    cur = connection.cursor()
    return connection, cur


def get_source_name():
    conn, cur = get_postgredb()
    cur.execute('SELECT source_name, id FROM spidersourcelist WHERE channel_id=35')
    rows = cur.fetchall()
    source_dict = dict()
    for i in rows:
        # source_name_list.append(i[0].decode('utf8'))
        source_dict[i[0].decode('utf8')] = i[1]

    conn.close()
    return source_dict


def add_spider_source(source_name):
    source_id = get_spider_source_max_id() + 1
    conn, cur = get_postgredb()
    ret = verify_exists_by_source_name(source_name)
    if ret:
        source_name = source_name + 'APP'
    cur.execute(
        '''INSERT INTO spidersourcelist (id, create_time, source_name, channel_name, channel_id, queue_name, frequency,status, online)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);''',
        (source_id, datetime.now(), source_name, 'APP', 35, 'spider:news:app:start_urls', 20, 0, 1))
    cur.execute(
        '''INSERT INTO sourcelist_v2 (id, ctime, sname, cname, cid, queue, rate, status, state)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);''',
        (source_id, datetime.now(), source_name, '点集', 35, 'spider:news:app:start_urls', 20, 0, 1)
    )
    conn.commit()
    conn.close()

    return source_id, source_name


def verify_exists_by_source_name(source_name):
    conn, cur = get_postgredb()
    cur.execute("SELECT count(*) FROM spidersourcelist WHERE source_name='%s' AND channel_id != 35" % source_name)
    rows = cur.fetchall()
    if rows[0][0]:
        return True
    return False


def get_spider_source_max_id():
    conn, cur = get_postgredb()
    cur.execute('SELECT max(id) FROM spidersourcelist')
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]


class Postgres(object):

    db_name = "BDP"
    db_user = "postgres"
    db_host = "120.27.163.25"
    db_password = "ly@postgres&2015"
    min_connections = 1
    max_connections = 5

    def __init__(self):
        self.pool = pool.SimpleConnectionPool(
            minconn=self.min_connections,
            maxconn=self.max_connections,
            database=self.db_name,
            user=self.db_user,
            host=self.db_host,
            password=self.db_password,
        )

    def run(self, sql):
        pass

    def query(self, sql):
        connection = self.pool.getconn()
        rows = list()
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
        except Exception, e:
            connection.rollback()
            print e
        finally:
            self.pool.putconn(connection)
        return rows

    def insert(self, sql):
        connection = self.pool.getconn()
        ret = False
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            ret = True
        except Exception, e:
            connection.rollback()
            print e
        finally:
            self.pool.putconn(connection)
            return ret

    def get_cur(self):
        connection = self.pool.getconn()
        cur = connection.cursor()
        return connection, cur

postgres = Postgres()

# print get_spider_source_max_id()
# print get_source_name()
# print add_spider_source('test')
# print verify_exists_by_source_name("'网易新闻'")
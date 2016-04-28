# coding=utf-8
from datetime import datetime

import psycopg2

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
        source_dict[i['0']] = i['1']

    conn.close()
    return source_dict


def add_spider_source(source_name):
    source_id = get_spider_source_max_id() + 1
    conn, cur = get_postgredb()
    ret = verify_exists_by_source_name(source_name)
    if ret:
        source_name = source_name + 'APP'
    cur.execute(
        '''INSERT INTO spidersourcelist (id, create_time, source_name, channel_name, channel_id, queue_name, frequency,status)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s);''',
        (source_id, datetime.now(), source_name, 'APP', 35, 'spider:news:app:start_urls', 20, 0))
    conn.commit()
    conn.close()
    return source_id, source_name


def verify_exists_by_source_name(source_name):
    conn, cur = get_postgredb()
    cur.execute('SELECT count(*) FROM spidersourcelist WHERE source_name=%s' % source_name)
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


# print get_spider_source_max_id()
# print get_source_name()
# print add_spider_source('test')
# print verify_exists_by_source_name("'网易新闻'")
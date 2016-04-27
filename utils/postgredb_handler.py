import psycopg2
from settings import *

from utils.utility import get_mongodb

def get_postgredb():
    connection = psycopg2.connect(database=POSTGRE_DBNAME, user=POSTGRE_USER, password=POSTGRE_PWD, host=POSTGRE_HOST,)
    cur = connection.cursor()
    return connection, cur


def get_source_name():
    conn, cur = get_postgredb()
    cur.execute('SELECT source_name from spidersourcelist GROUP BY source_name')
    rows = cur.fetchall()
    source_name_list = list()
    for i in rows:
        source_name_list.append(i[0].decode('utf8'))
    conn.close
    return source_name_list


def add_spider_source(source_name):
    conn, cur = get_postgredb()
    cur.execute('INSERT INTO spidersourcelist (create_time, source_name, channel_name, channel_id, queue_name, frequency,\
status, )')


print get_source_name()
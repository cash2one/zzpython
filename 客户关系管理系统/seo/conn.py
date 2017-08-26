# -*- coding: utf-8 -*-
import MySQLdb
import pymongo
from DBUtils.PooledDB import PooledDB
from MySQLdb.cursors import DictCursor


def open_db():
    """
    :return: 返回数据库连接
    """
    # 不使用连接池的MySQL连接方法
    # conn = MySQLdb.connect(host="192.168.2.4", port=3306, user="zz91crm", passwd="zJ88friend",
    # db="zz91crm", charset="utf8")
    # cur = conn.cursor()

    # 使用连接池的方法
    # 不设置charset，读出来的是乱码
    pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=5, maxshared=10, maxconnections=5,
                    host="192.168.2.4", port=3306, user="zz91crm", passwd="zJ88friend",
                    db="zz91crm", charset="utf8")
    conn = pool.connection()
    return conn


def fetch_all(sql, *args):
    """
    :param sql: 查询语句
    :param args: 需要的参数
    :return: 返回所有符合条件的数据
    """
    conn = open_db()
    cur = conn.cursor(DictCursor)
    cur.execute(sql, *args)
    r = cur.fetchall()
    cur.close()
    conn.close()
    return r


def fetch_one(sql, *args):
    """
    :param sql: 写好的查询语句
    :param args: 需要的参数
    :return: 返回一条符合条件的语句
    """
    conn = open_db()
    cur = conn.cursor(DictCursor)
    cur.execute(sql, *args)
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r


def update_db(sql, *args):
    # 更新、插入、删除等功能
    # r返回最后一个插入的id
    conn = open_db()
    cur = conn.cursor(DictCursor)
    try:
        cur.execute(sql, *args)
        cur.execute('select last_insert_id() as id')
        r = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return r
    except Exception:
        conn.rollback()


def get_count(sql, *args):
    # 返回sql语句查询出的总条数
    conn = open_db()
    cur = conn.cursor(DictCursor)
    cur.execute(sql, *args)
    return cur.rowcount


def conn_mongodb():
    # 连接mongodb,数据库为richangts
    client = pymongo.MongoClient(host='192.168.2.4', port=27017)
    db = client.richangts
    return db


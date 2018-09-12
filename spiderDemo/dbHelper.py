# encoding: utf-8
import time

import pymysql

pymysql.install_as_MySQLdb()
from scrapy.utils.project import get_project_settings


class DbHelper:
    def __init__(self):
        self.settings = get_project_settings()

        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings['MYSQL_USER']
        self.passwd = self.settings['MYSQL_PASSWD']
        self.db = self.settings['MYSQL_DBNAME']

    def connect_mysql(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db,
                               charset='utf8')
        return conn

    def insert(self, sql, *params):  # 注意这里params要加*,因为传递过来的是元组，*表示参数个数不定
        conn = self.connect_mysql()
        cur = conn.cursor();
        cur.execute(sql, params)
        conn.commit()  # 注意要commit
        cur.close()
        conn.close()

    def select(self, sql, *params):
        conn = self.connect_mysql()
        cur = conn.cursor()
        count = cur.execute(sql, params)
        fc = cur.fetchall()
        cur.close()
        conn.close()
        return fc

    def update(self, sql, *params):
        conn = self.connect_mysql()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def select_url_config(self, start_row, row_size):
        sql = "select * from demo_db  limit %s ,%s "
        params = (int(start_row), int(row_size))
        msg = self.select(sql, *params)
        return msg

    def update_url_config(self, ids):
        sql = "update demo_db set  update_time=%s  where id = %s "
        params = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), int(ids))
        self.update(sql, *params)

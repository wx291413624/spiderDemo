# coding=utf8
import random
import time

import logging
import logging.handlers
import urllib

import schedule

import sys

reload(sys)
sys.setdefaultencoding('utf8')

logs = logging.getLogger(__name__)
logs.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler(
    '/tmp/ipConfig.log', maxBytes=10000000, backupCount=5)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(u'%(asctime)s [%(levelname)s] %(message)s')
fh.setFormatter(formatter)
logs.addHandler(fh)

order = "8eb1b6753a6652c56f1a05f132cb304f"
apiUrl = "http://dynamic.goubanjia.com/dynamic/get/" + order + ".html"


def job():
    try:
        logs.info(random.randint(0, 9))
        logs.info("start---------")
        res = urllib.urlopen(apiUrl).read().strip("\n")
        ips = res
        fo = open("/tmp/ipConfig.txt", "w")
        fo.write(str(ips))
        fo.close()
        logs.info("ip===:" + str(ips))
        logs.error("----over")
    except Exception as e:
        logs.error("执行异常")
        logs.error(e)


job()
schedule.every(5).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)

# coding=utf-8
import logging

import time
import urllib

logger = logging.getLogger(__name__)


def getIp():
    order = "8eb1b6753a6652c56f1a05f132cb304f"
    apiUrl = "http://dynamic.goubanjia.com/dynamic/get/" + order + ".html"
    try:
        ress = urllib.urlopen(apiUrl).read().strip("\n")
        print("---???---" + ress)
        if "too many requests".startswith(ress):
            logger.info("-------------too many requests---------------------")
            time.sleep(6)
            return getIp()
        else:
            logger.info("-------------ip 代理获取-------------------")
            return ress
    except Exception as e:
        print(e)
        logger.info("-----------------:ip获取异常 睡眠五秒:-----------------")
        time.sleep(6)
        logger.info("-----------------:ip获取异常:-----------------")
        return getIp()

# def getHtmlIp():
#     targetUrl = "http://1212.ip138.com/ic.asp"
#     ip=getIp()
#     logger.info(ip)
#     proxy_handler = urllib2.ProxyHandler({
#         'http': 'http://' + ip
#     })
#     opener = urllib2.build_opener(proxy_handler)
#     html = opener.open(targetUrl)
#     print(html.read().decode("utf-8"))

#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import time
from twisted.web._newclient import ResponseNeverReceived
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError

from spiderDemo.ip_config.get_file_ip_config import find_ip

logger = logging.getLogger(__name__)


class HttpProxyMiddleware(object):
    DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError)

    def __init__(self, settings):
        self.new_proxyes = find_ip()
        logger.info("======================初始化====================")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def fetch_new_proxyes(self):
        self.new_proxyes = find_ip()

    def set_proxy(self, request):
        request.meta["proxy"] = "http://" + self.new_proxyes
        logger.info("--------------当前代理--------------")
        logger.info(request.meta["proxy"])

    def process_request(self, request, spider):
        logger.info("设置代理-----------------------")
        if not self.new_proxyes:
            self.fetch_new_proxyes()
        self.set_proxy(request)
        request.meta["dont_redirect"] = True  # 有些代理会把请求重定向到一个莫名其妙的地址
        logger.info(request.meta)
        if "change_proxy" in request.meta.keys() and request.meta["change_proxy"]:
            self.set_proxy(request)
            request.meta["change_proxy"] = False

    def process_response(self, request, response, spider):
        logger.info("--------RESPONSE STATUS-----------------------" + str(response.status))
        logger.debug(response.body)

        if response.status != 200:
            self.fetch_new_proxyes()
            time.sleep(5)
            self.set_proxy(request)
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request
        else:
            logger.info("-----------------SUCCESS RESPONSE---------------------")
            return response

    def process_exception(self, request, exception, spider):
        logger.info("-----------REQUEST ERROR-----------------")
        self.new_proxyes = None
        logger.debug(exception)
        if isinstance(exception, self.DONT_RETRY_ERRORS):
            self.fetch_new_proxyes()
            self.set_proxy(request)
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request

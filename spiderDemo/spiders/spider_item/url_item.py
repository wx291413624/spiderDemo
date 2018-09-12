# encoding: utf8
import json

import scrapy
import logging

import sys

from spiderDemo.dbHelper import DbHelper
from spiderDemo.items import SpiderdemoItem

reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger(__name__)


class CrawlSpider(scrapy.Spider):
    name = "spider_url_item"

    def start_requests(self):
        url_config = DbHelper().select_url_config(1500, 500)
        for url in url_config:
            url = """https://demo.com""" + url[0]
            yield scrapy.FormRequest(
                method="GET",
                url=url,
                formdata={},
                callback=self.parse
            )

    def parse(self, response):
        logger.info("返回结果-------------------")
        response_body = response.body
        is_true = self.findjson(response_body)
        if is_true:
            we = SpiderdemoItem()
            we["body"] = response_body
            return we
        else:
            return None

    def findjson(self, myjson):
        try:
            json.loads(myjson)
        except ValueError:
            return False
        return True

import logging

from settings import USER_AGENT_LIST

import random

logger = logging.getLogger(__name__)


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            logger.info("------------------set user agent ")
            logger.debug(ua)
            request.headers.setdefault('User-Agent', ua)

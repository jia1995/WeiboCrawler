# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import base64 
from scrapy import signals
from scrapy.http import Request, FormRequest
from Spider.settings import USER_AGENT
from Spider.get_proxy import get_proxies

Proxy = [
    '123.163.163.60:34181',
]

url = 'http://cn-proxy.com/'

class Proxy_And_UsrAgent(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def process_request(self,request,spider):
        request.headers.setdefault('User-Agent',random.choice(USER_AGENT))
        #request.meta['proxy'] = 'http://' + random.choice(get_proxies(url))
        #request.meta['proxy'] = 'http://' + random.choice(Proxy)
    

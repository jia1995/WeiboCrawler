# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboSearchItem(scrapy.Item):
    Usr_ID = scrapy.Field() #用户ID
    Usr_Info = scrapy.Field() #用户信息
    Num_Post = scrapy.Field() #发送微博数量
    Num_Follows = scrapy.Field() #关注者数
    Num_Fans = scrapy.Field() #粉丝数

# -*- coding: utf-8 -*-
import pymysql
import datetime
from weibo_Search.items import WeiboSearchItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class WeiboSearchPipeline(object):
    conn = object()
    cur = object()

    def __init__(self):
        try:
            self.conn = pymysql.connect(host="localhost",user="root",passwd="123abc456",db="weibo",charset="utf8")
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Failed to Get SQL!")
            exit(1)

    def Submit(self,item):
        sql = "INSERT INTO Weibo_Profile (UID, Usr_Info, Num_Post, Num_Fans, Num_Follows, Collect_Time) VALUES (%s, %s, %s, %s, %s, str_to_date(%s,'%%Y-%%m-%%d'))"
        self.cur.execute(sql,(item['Usr_ID'],item['Usr_Info'],
        item['Num_Post'],item['Num_Fans'],
        item['Num_Follows'],datetime.date.today()))
        self.conn.commit()
    
    def process_item(self, item, spider):
        if item != None:
            try:
                self.Submit(item)
                return 'SQL Sending Successfully.'
            except Exception as e:
                return e
        return

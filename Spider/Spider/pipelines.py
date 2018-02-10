# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import datetime
from Spider.items import UsrInfo
from Spider.items import PipeItem

from weibo_api.client import WeiboClient

class StitchPipeline(object):
    UID_Dic = {}
    def process_item(self,item,spider):
        if item['Usr_ID'] not in self.UID_Dic.keys():
            Usr = UsrInfo()
            Usr['Fans_List'] = []
            Usr['Follows_List'] = []
            Usr['Usr_ID'] = item['Usr_ID']
            self.UID_Dic[item['Usr_ID']] = [1,Usr]
            self.UID_Dic[item['Usr_ID']][0] = 0
        if item['Item_Type'] == 0: #Get Follows
                self.UID_Dic[item['Usr_ID']][1]['Follows_List'] += item['Datagram']
        elif item['Item_Type'] == 1: #Get Fans
            self.UID_Dic[item['Usr_ID']][1]['Fans_List'] = item['Datagram']
        elif item['Item_Type'] == 2: #Get Info
            self.UID_Dic[item['Usr_ID']][1]['Usr_Info'] = item['Datagram'][0]
            self.UID_Dic[item['Usr_ID']][1]['Num_Follows'] = item['Datagram'][1]
            self.UID_Dic[item['Usr_ID']][1]['Num_Fans'] = item['Datagram'][2]
            self.UID_Dic[item['Usr_ID']][1]['Num_Post'] = item['Datagram'][3]
        else:
            exit(1)
        self.UID_Dic[item['Usr_ID']][0] = self.UID_Dic[item['Usr_ID']][0] + 1
        if self.UID_Dic[item['Usr_ID']][0] == 3:
            Usr = self.UID_Dic[item['Usr_ID']][1]
            del self.UID_Dic[item['Usr_ID']]
            return Usr
        else:
            pass

class SpiderPipeline(object):
    Cur = object()   #SQL
    Conn = object()  #SQL
    #client = object()
    def __init__(self):
        try:
            self.Conn = pymysql.connect(host="localhost",user="root",passwd="123abc456",db="weibo_test",charset="utf8")
            self.Cur = self.Conn.cursor()
            #self.client = WeiboClient()
        except Exception as e:
            print('Failed to Get SQL!')
            exit(1)

    def Submit(self,item):
        sql = "INSERT INTO Weibo_Profile (UID, Usr_Info, Num_Post, Num_Fans, Num_Follows, Collect_Time) VALUES (%s, %s, %s, %s, %s, str_to_date(%s,'%%Y-%%m-%%d'))"
        self.Cur.execute(sql,(item['Usr_ID'],item['Usr_Info'],
        item['Num_Post'],item['Num_Fans'],
        item['Num_Follows'],datetime.date.today()))
        self.Conn.commit()
    '''
    def SubmitContext(self,UID):
        psql = "insert into weibo_context(uid,cid,context,time) values (%s,%s,%s,%s)"
        p = self.client.people(UID)
        for status in p.statuses.page(1):
           self.Cur.execute("set names utf8mb4")
           self.Cur.execute(psql,(UID,format(status.id),format(status.text),format(status.created_at)))
           self.Conn.commit()
    '''
    def process_item(self, item, spider):
        if item != None:
            if '湖北' in item['Usr_Info']:
                try:
                    self.Submit(item)
                    #self.SubmitContext(item['Usr_ID'])
                    return 'SQL Sending Successfully.'
                except Exception as e:
                    return e
        return

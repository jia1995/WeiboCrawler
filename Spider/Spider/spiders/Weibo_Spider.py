# encoding: utf-8
from scrapy.http import Request, FormRequest
from Spider.items import PipeItem
from Spider.cookies import get_cookie_from_weibo
import scrapy
import re
import bs4

Max_Waited_Length = 1000
Account_Cookies = []
Header = {
    "Host":
    "weibo.cn",
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language":
    "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding":
    "gzip, deflate",
}

def GetPostInfo(self, Info):
    return ''

class WeiboSpiderSpider(scrapy.Spider):
    name = "Weibo_Spider"
    Completed_UID = ['6449959454']
    Task_In_Queue = 1
    Account_Cookies.append(get_cookie_from_weibo('18229918002','ttk1125'))
    def start_requests(self):
        return [
            Request('https://weibo.cn/' + self.Completed_UID[0] + '/fans',cookies=Account_Cookies[0],meta=Header,callback=self.GetFollowers)
            #Request('http://www.ipip.net/',callback=self.Show_IP)
        ]
    def Show_IP(self,response):
        soup = bs4.BeautifulSoup(response.body.decode(response.encoding),'lxml')
        print(response.body.decode('utf-8', 'ignore').replace(u'\xa9', u''))

    def Get_PipeItem(self,response,Item_Type):
        Pipe_Item = PipeItem()
        Pipe_Item['Item_Type'] = Item_Type # 1 is get followers list
        Pipe_Item['Datagram'] = []
        Pipe_Item['Usr_ID'] = []
        Pipe_Item['Usr_ID'] = str(re.search('[0-9]{10}',str(response.url)).group())
        return Pipe_Item
    
    def GetFollowers(self, response):
        if(response.status == 403):
            exit(1)
        Pipe_Item = self.Get_PipeItem(response,0)
        self.Task_In_Queue = self.Task_In_Queue - 1
        soup = bs4.BeautifulSoup(response.body.decode(response.encoding),'lxml')
        Tag = soup.table
        while Tag != None:
            try:
                if(str(Tag.a) != None):
                    UID = re.search("/u/[0-9]{10}",str(Tag.a))
                    if UID != None:
                        Pipe_Item['Datagram'].append(str(UID.group())[3:])
                Tag = Tag.next_sibling
            except Exception as e: #Not a Tag but a Navigate
                Tag = Tag.next_sibling
                continue
        for rUID in Pipe_Item['Datagram']:
            if rUID in self.Completed_UID:
                continue
            else:
                if self.Task_In_Queue > Max_Waited_Length :
                    break
                else:
                    self.Completed_UID.append(rUID)
                    self.Task_In_Queue = self.Task_In_Queue + 1
                    yield Request('https://weibo.cn/u/' + rUID ,cookies=Account_Cookies[0],meta=Header,callback=self.GetUsrInfo)
                    yield Request('https://weibo.cn/' + rUID + '/fans',cookies=Account_Cookies[0],meta=Header,callback=self.GetFans)
                    yield Request('https://weibo.cn/' + rUID + '/follow',cookies=Account_Cookies[0],meta=Header,callback=self.GetFollowers)
        yield Pipe_Item
    def GetFans(self, response):
        if(response.status == 403):
            exit(1)
        Pipe_Item = self.Get_PipeItem(response,1)
        self.Task_In_Queue = self.Task_In_Queue - 1
        soup = bs4.BeautifulSoup(response.body.decode(response.encoding),'lxml')
        Tag = soup.table
        while Tag != None:
            try:
                if(str(Tag.a) != None):
                    UID = re.search("/u/[0-9]{10}",str(Tag.a))
                    if UID != None:
                        Pipe_Item['Datagram'].append(str(UID.group())[3:])
                Tag = Tag.next_sibling
            except Exception as e: #Not a Tag but a Navigate
                Tag = Tag.next_sibling
                continue
        yield Pipe_Item

    def GetUsrInfo(self, response):
        if(response.status == 403):
            exit(1)
        Pipe_Item = self.Get_PipeItem(response,2)
        self.Task_In_Queue = self.Task_In_Queue - 1
        soup = bs4.BeautifulSoup(response.body.decode(response.encoding), 'lxml')
        Info = soup.find('span', class_='ctt')
        Pipe_Item['Datagram'].append(str(Info.text).replace('\xa0',' ')[:-12])
        Pipe_Item['Datagram'].append(re.search('关注\[\d+\]',str(soup.text)).group()[3:-1])
        Pipe_Item['Datagram'].append( re.search('粉丝\[\d+\]',str(soup.text)).group()[3:-1])
        Pipe_Item['Datagram'].append(re.search('微博\[\d+\]',str(soup.text)).group()[3:-1])
        yield Pipe_Item

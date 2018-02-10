# encoding: utf-8
from scrapy.http import Request, FormRequest
from weibo_Search.cookies import get_cookie_from_weibo
from weibo_Search.items import WeiboSearchItem
import scrapy
import re
import bs4

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

class WeiboSearchSpider(scrapy.Spider):
    name = "Weibo_Search"
    City_Type = [] #；城市代码
    Gender_Type = [1,2]
    Province = 42#城市代码，默认为湖北42
    cookie = get_cookie_from_weibo('微博账号','账号密码')
    def start_requests(self):
        return[
            Request('https://weibo.cn/find/city/?province='+Province,cookies=self.cookie,meta=Header,callback=self.SetCity)
            ]

    def GetItem(self):
        Item = Item = WeiboSearchItem()
        Item['Usr_ID'] = []
        Item['Usr_Info'] = []
        Item['Num_Follows'] = []
        Item['Num_Fans'] = []
        Item['Num_Post'] = []
        return Item

    def SetCity(self,response):
        for City in self.City_Type:
            yield Request(str(response.url)+'&city='+str(City),cookies=self.cookie,meta=Header,callback=self.SetGender)

    def SetGender(self,response):
        for Gender in self.Gender_Type:
            yield Request(str(response.url)+'&gender='+str(Gender),cookies=self.cookie,meta=Header,callback=self.SetPage)

    def SetPage(self, response):
        i = 1
        while i < 51:
            yield Request(str(response.url)+'&page='+str(i),cookies=self.cookie,meta=Header,callback=self.getUID)
            i=i+1

    def GetUsrInfo(self, response):
        if(response.status == 403):
            exit(1)
        Item=self.GetItem()
        UID = str(re.search('[0-9]{10}',str(response.url)).group())
        soup = bs4.BeautifulSoup(response.body.decode(response.encoding), 'lxml')
        Info = soup.find('span', class_='ctt')
        Item['Usr_ID'].append(UID)
        Item['Usr_Info'].append(str(Info.text).replace('\xa0',' ')[:-12])
        Item['Num_Follows'].append(re.search('关注\[\d+\]',str(soup.text)).group()[3:-1])
        Item['Num_Fans'].append( re.search('粉丝\[\d+\]',str(soup.text)).group()[3:-1])
        Item['Num_Post'].append(re.search('微博\[\d+\]',str(soup.text)).group()[3:-1])
        yield Item

    def getUID(self,response):
        soup = bs4.BeautifulSoup(response.body.decode('utf-8'), 'lxml')
        Tag = soup.table
        i = 1
        UIDs = []
        while Tag != None:
            try:
                if(str(Tag.form) != None):
                    UID = re.search("uid=[0-9]{10}",str(Tag.form))
                    print(UID)
                    if UID != None:
                        rUID = str(UID.group())[4:]
                        UIDs.append(rUID)
                Tag = Tag.next_sibling
            except Exception as e:
                Tag = Tag.next_sibling
                continue
        for UID in UIDs:
            yield Request('https://weibo.cn/u/'+UID,cookies=self.cookie,meta=Header,callback=self.GetUsrInfo)

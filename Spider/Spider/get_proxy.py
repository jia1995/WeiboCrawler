# -*- coding: utf-8 -*-
# Python:      2.7.8
# Platform:    Windows
# Author:      wucl
# Program:     从代理网站获取可用代理
# History:     2015.6.11
 
 
import urllib.request, re
from bs4 import BeautifulSoup
 
def get_proxies(url):
    """
    从代理网站获取可用代理ip地址列表并返回
    """
    resp = urllib.request.urlopen(url)
    html = resp.read()
    soup = BeautifulSoup(html,'lxml')
    contents = soup.find_all('tr')
    regex = re.compile('\d+')
    proxies = []
    for each in contents:
        sock = each.find_all('td')
        if sock:
            ip = sock[0].text
            port = sock[1].text
            if re.findall(regex, ip):
                proxy = '%s:%s' %(ip, port)
                proxies.append(proxy)
    return proxies
 
 
 
#if __name__ == '__main__':
#    url = 'http://cn-proxy.com/'
#    proxies = get_proxies(url)
#    print proxies

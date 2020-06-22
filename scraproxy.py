import requests, traceback
from lxml.html import fromstring
from itertools import cycle

def get_infoFrom(url, key):
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:1000]:
        if i.xpath('.//td[7][contains(text(),"yes")]') and key == 0:
            proxy = ";".join(["https",i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
        elif i.xpath('.//td[7][contains(text(),"no")]') and key == 0:
            proxy = ";".join(["http",i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
        elif i.xpath('.//td[7][contains(text(),"Yes")]') and key == 1:
            proxy = ";".join([i.xpath('.//td[5]/text()')[0],i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

def launcher():
    with open('list.csv', 'a') as file:
        for elem in get_infoFrom("https://free-proxy-list.net/", 0):
            file.write('%s\n' % elem)
        for elem in get_infoFrom("https://www.socks-proxy.net/", 1):
            file.write('%s\n' % elem)



def main():
    launcher()

if __name__== "__main__":
  main()

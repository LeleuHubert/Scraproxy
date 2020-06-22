from lxml.html import fromstring
import requests
from itertools import cycle
import traceback

def get_infoFrom(url):
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ";".join(["https",i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
        elif i.xpath('.//td[7][contains(text(),"no")]'):
            proxy = ";".join(["http",i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def main():
    info = get_infoFrom("https://free-proxy-list.net/")

    with open('list.csv', 'a') as file:
        for elem in info:
            file.write('%s\n' % elem)

if __name__== "__main__":
  main()

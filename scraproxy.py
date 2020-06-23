import requests, traceback, cloudscraper, re
from lxml.html import fromstring
from itertools import cycle

def next_page(url, info):
    pages = []

    for i in range(1, info[0]+1, info[1]):
        if info[2] == 0:
            j = url + str(i)
        elif info[2] == 1:
            j = url + "0" + str(i) + ".htm"
        pages.append(j)

    return pages

def get_info(parser, proxies, key):
    for i in parser.xpath('//tbody/tr')[:300]:
        if i.xpath('.//td[7][contains(text(),"yes")]') and key == 0:
            proxy = ";".join(["https",i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
        elif i.xpath('.//td[7][contains(text(),"no")]') and key == 0:
            proxy = ";".join(["http",i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
        elif key == 1:
            proxy = ";".join([i.xpath('.//td[5]/text()')[0], i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
        elif key == 2: #type proxy doublons sur la ligne
            if i.xpath('.//td[5]/text()')[0].find(", ") == -1:
                proxy = ";".join([i.xpath('.//td[5]/text()')[0], i.xpath('.//td[1]/text()')[0], i.xpath(".//td[2]/text()")[0]])
                proxies.add(proxy)
    return proxies

def get_infoFrom(url, key):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    parser = fromstring(response.text)
    proxies = set()
    proxies = get_info(parser, proxies, key)
    return proxies

def cleaner(proxies):
    proxies = [proxy.replace(';', ':') for proxy in proxies]
    proxies = [proxy.replace('https:', '') for proxy in proxies]
    proxies = [proxy.replace('http:', '') for proxy in proxies]

    return proxies

def tester(proxies):
    print(proxies)


def launcher():
    proxiAdrss = []

    print("- scrapping step starting")
    with open('list.csv', 'a') as file:
        for elem in get_infoFrom("https://free-proxy-list.net/", 0):
            proxiAdrss.append(elem)
            file.write('%s\n' % elem)
        for elem in get_infoFrom("https://www.socks-proxy.net/", 1):
            proxiAdrss.append(elem)
            file.write('%s\n' % elem)
        # for page in next_page("https://hidemy.name/en/proxy-list/?start=", [1216,64,0]):
        #     for elem in get_infoFrom(page, 2):
        #         proxiAdrss.append(elem)
        #         file.write('%s\n' % elem)
    print("- testing step starting")
    tester(cleaner(proxiAdrss))

def main():
    print("-> Scraproxy has started")
    launcher()
    print("-> Scraproxy's over")

if __name__== "__main__":
  main()

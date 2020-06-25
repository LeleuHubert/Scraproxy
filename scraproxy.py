import requests, traceback, cloudscraper, re, sys
from requests.exceptions import ProxyError, Timeout, InvalidProxyURL
from lxml.html import fromstring
from itertools import cycle

def areyouconnected():
    try:
        rep = requests.get("http://ifconfig.me/ip")
        if rep:
            print("[",  rep.text, "] -> Scraproxy has started")
            return rep.text
        else:
            print("You don't seem to be connected to the internet.")
            return 1
    except:
        return 1

def next_page(url, info):
    pages = []

    for i in range(1, info[0]+1, info[1]):
        if info[2] == 0:
            j = url + str(i)
        elif info[2] == 1:
            j = url + "0" + str(i) + ".htm"
        pages.append(j)

    return pages

def get_info(parser, proxies, key, nbr):
    for i in parser.xpath('//tbody/tr')[:nbr]:
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

def get_infoFrom(url, key, nbr):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    parser = fromstring(response.text)
    proxies = set()
    proxies = get_info(parser, proxies, key, nbr)
    return proxies

def fileCreator(proxies):
    with open('working.csv', 'a') as file:
        for proxy in proxies:
            file.write('%s\n' % proxy)

def cleaner(proxies, key):
    if key == 0:
        proxies = [proxy.replace(';', ':') for proxy in proxies]
        proxies = [proxy.lower() for proxy in proxies]
        proxies = [proxy.replace('https:', 'https://') for proxy in proxies]
        proxies = [proxy.replace('http:', 'http://') for proxy in proxies]
        proxies = [proxy.replace('socks4:', 'socks4://') for proxy in proxies]
        proxies = [proxy.replace('socks5:', 'socks5://') for proxy in proxies]
    elif key == 1:
        proxies = [proxy.replace(':', ';') for proxy in proxies]
        proxies = [proxy.lower() for proxy in proxies]
        proxies = [proxy.replace('socks4;//', 'socks4;') for proxy in proxies]
        proxies = [proxy.replace('socks5;//', 'socks5;') for proxy in proxies]

    return proxies

def tester(proxies, ip, ref_IPs):
    whitelist = []
    proxy_pool = cycle(proxies)

    for i in range(1, len(proxies)):
        proxy = next(proxy_pool)
        print("                          ", end="\r")
        print("- please wait ", len(proxies)-i, end="\r")
        try:
            rep = requests.get("http://ifconfig.me/ip", proxies={"http": proxy, "https": proxy}, timeout=1)
            if rep.status_code == 200:
                whitelist.append(ref_IPs[i])
        except:
            pass

    fileCreator(cleaner(whitelist, 1))

def launcher(nbr):
    ip = areyouconnected()
    list_IPs = []
    good_IP = []
    count = 0

    if ip != 1:
        print("- step n°1 start    (scrapping)")
        for elem in get_infoFrom("https://free-proxy-list.net/", 0, nbr):
            list_IPs.append(elem)
        for elem in get_infoFrom("https://www.socks-proxy.net/", 1, nbr):
            list_IPs.append(elem)
        for page in next_page("https://hidemy.name/en/proxy-list/?start=", [576,64,0]):
            for elem in get_infoFrom(page, 2, nbr):
                list_IPs.append(elem)
        with open('list.csv', 'w') as fp:
            for ipline in list_IPs:
                fp.write('%s\n' % ipline)
                good_IP.append(ipline)
        print("- step n°2 start    (testing)")
        list_IPs = good_IP
        tester(cleaner(good_IP, 0), ip, list_IPs)
    else:
        print("- end of execution of Scraproxy")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        a = int(sys.argv[1])
        launcher(a)
    else:
        launcher(100)

    print("----> Scraproxy's over")

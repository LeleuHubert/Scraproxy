import requests, traceback, cloudscraper, re, sys
from lxml.html import fromstring
from itertools import cycle

def areyouconnected():
    try:
        rep = requests.get("http://ifconfig.me/ip")
        if rep:
            print("-> Scraproxy has started with IP [ ", rep.text, " ]")
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
        proxies = [proxy.replace('https:', '') for proxy in proxies]
        proxies = [proxy.replace('http:', '') for proxy in proxies]
        proxies = [proxy.replace('Socks4:', 'socks4://') for proxy in proxies]
        proxies = [proxy.replace('Socks5:', 'socks5://') for proxy in proxies]
    elif key == 1:
        proxies = [proxy.replace(':', ';') for proxy in proxies]
        proxies = [proxy.replace('socks4;//', 'socks4;') for proxy in proxies]
        proxies = [proxy.replace('socks5;//', 'socks5;') for proxy in proxies]
        # proxies = [proxy.replace('', '') for proxy in proxies] #http & https

    return proxies

def tester(proxies, ip):
    whitelist = []

    for proxy in proxies:
        try:
            rep = requests.get("http://ifconfig.me/ip", {'http': proxy, 'https': proxy})
            if rep.text == ip:
                whitelist.append(proxy)
            else:
                proxies.remove(proxy)
        except:
            proxies.remove(proxy)
    fileCreator(cleaner(whitelist, 1))

def launcher(nbr):
    proxiAdrss = []
    ip = areyouconnected()

    if ip != 1:
        print("- step n°1 start    (scrapping)")
        with open('list.csv', 'a') as file:
            for elem in get_infoFrom("https://free-proxy-list.net/", 0, nbr):
                proxiAdrss.append(elem)
                file.write('%s\n' % elem)
            for elem in get_infoFrom("https://www.socks-proxy.net/", 1, nbr):
                proxiAdrss.append(elem)
                file.write('%s\n' % elem)
            # for page in next_page("https://hidemy.name/en/proxy-list/?start=", [1216,64,0]):
            #     for elem in get_infoFrom(page, 2, nbr):
            #         proxiAdrss.append(elem)
            #         file.write('%s\n' % elem)
        print("- step n°1 done\n- step n°2 start    (testing)")
        tester(cleaner(proxiAdrss, 0), ip)
        print("- step n°2 done")
    else:
        print("- end of execution of Scraproxy")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        a = int(sys.argv[1])
        launcher(a)
    else:
        launcher(100)

    print("-> Scraproxy's over")

import time, bs4, random, requests, cloudscraper, csv, re
from fake_useragent import UserAgent
import itertools as it
import pandas as pd

def get_pages(token):
    pages = []
    for i in range(1, token[1]+1, token[2]):
        if token[1] != 1 and token[3] == 0:
            j = token[0] + str(i)
        elif token[1] != 1 and token[3] == 1:
            j = token[0] + "0" + str(i) + ".htm"
        else:
            j = token[0]
        pages.append(j)
    return pages

def parseLine(line):
    rx = re.compile(r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)')
    stock = []

    for ip in rx.findall(str(line)):
        stock.append(ip)

    with open('list.csv', 'a') as file:
        for elem in stock:
            file.write('%s\n' % elem)

def connector(i, proxy, ua, pattern):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(i, proxies={"http": proxy, "https": proxy}, headers={'User-Agent': ua.random}, timeout=5)
    time.sleep(random.randrange(1,4))
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    if pattern[1] != "null":
        return soup.find_all(pattern[0], {"class":pattern[1]})
    else:
        return soup.find_all("tr")

def get_data(pages, proxies, pattern):
    df = pd.DataFrame()
    ua = UserAgent()
    proxy_pool = it.cycle(proxies)
    lock = -1
    print("please wait few second")
    while len(pages) > 0:
        for i in pages:
            df_f = pd.DataFrame()
            if lock < 1:
                proxy = next(proxy_pool)
            try:
                lock = 1
                tr_box = connector(i, proxy, ua, pattern)

                if len(tr_box) != 0:
                    for l in tr_box:
                        parseLine(l)
                    pages.remove(i)
                else:
                    print("Alert: ", len(tr_box), " element found")
            except:
                lock = 0

    return df

def launcher(proxies):
    token0 = ["http://nntime.com/proxy-list-", 7, 1, 1, ["tr", "odd"]] ### pas de port indiqué ###
    token1 = ["http://nntime.com/proxy-list-", 7, 1, 1, ["tr", "even"]] ### pas de port indiqué ###
    token2 = ["https://hidemy.name/en/proxy-list/?start=", 128, 64, 0, ["tr","null"]] ###CLOUDFLARE PROTECTION###

    token3 = ["https://www.ip-adress.com/proxy-list", 1, 1, 0, ["tr","null"]]
    token4 = ["http://free-proxy.cz/en/proxylist/main/", 150, 1, 0, ["tr","null"]] ###CAPTCHAT###
    token5 = ["https://www.proxynova.com/proxy-server-list/anonymous-proxies/", 1, 1, 0, ["tr", "data-proxy-id"]]

    tokens = [token2]
    for tok in tokens:
        get_data(get_pages(tok), proxies, tok[4])

def main():
    proxies = pd.read_csv('Proxy_List.txt', header = None)
    proxies = proxies.values.tolist()
    proxies = list(it.chain.from_iterable(proxies))

    print("Scraproxy is starting\n->", end=" ")
    launcher(proxies)
    print("- - - - - FINISH - - - - -")

if __name__== "__main__":
  main()

import pandas as pd
import time
import bs4
import random
import requests
from fake_useragent import UserAgent
import itertools as it
import cloudscraper
import csv

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
    stock = []

    for balise in line:
        for content in balise:
            stock.append(content)
    print("- step n°3 done [", len(stock), "]")

def connector(i, proxy, ua):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(i, proxies={"http": proxy, "https": proxy}, headers={'User-Agent': ua.random}, timeout=5)
    time.sleep(random.randrange(1,4))
    print("- connection done")
    return bs4.BeautifulSoup(response.text, 'html.parser')

def get_data(pages,proxies):
    df = pd.DataFrame()
    param = ['td']
    ua = UserAgent()
    proxy_pool = it.cycle(proxies)
    lock = -1

    while len(pages) > 0:
        for i in pages:
            df_f = pd.DataFrame()
            if lock < 1:
                proxy = next(proxy_pool)
                print("\n( ", proxy, " ) :")
            try:
                soup = connector(i, proxy, ua)
                lock = 1
                tr_box = soup.find_all("tr")
                print("- step n°2 done [", len(tr_box), "]")

                for l in tr_box:
                    parseLine(l)
                print(len(pages), " pages left to analyze.")
                pages.remove(i)

            except requests.Timeout as err:
                lock = 0
            except:
                print(err.message)

    return df

def launcher(proxies):
    token0 = ["http://nntime.com/proxy-list-", 7, 1, 1]
    token1 = ["https://hidemy.name/fr/proxy-list/?start=", 1280, 64, 0] ###CLOUDFLARE PROTECTION###
    token2 = ["https://www.ip-adress.com/proxy-list", 1, 1, 0]
    token3 = ["http://free-proxy.cz/en/proxylist/main/", 150, 1, 0] ###CAPTCHAT###

    tokens = [token0]
    for tok in range(0, len(tokens)):

        get_data(get_pages(tokens[tok]),proxies)

def main():
    proxies = pd.read_csv('Proxy_List.txt', header = None)
    proxies = proxies.values.tolist()
    proxies = list(it.chain.from_iterable(proxies))

    print("Scraproxy is starting")
    launcher(proxies)
    print("Scraproxy's over")

if __name__== "__main__":
  main()

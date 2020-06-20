import pandas as pd
import time
import bs4
import random
import requests
from fake_useragent import UserAgent
import itertools as it
import cloudscraper

def get_pages(token, nb, jump):
    pages = []
    for i in range(1, nb+1, jump):
        if nb != 1:
            j = token + str(i)
        else:
            j = token
        pages.append(j)
    print("Scraproxy detected ", len(pages) ," pages on ", token)
    return pages

def parseLine(line):
    elem = []
    a = 0

    print("begin of parseLine")

    for l in range(0, line+1, 1):
        if (line[l] == '>'):
            save = 1
        elif (save == 1):
            print(line[l])
            elem[a] = line[l]
            a += 1
        elif (line[l] == "<"):
            save = 0
            print(''.join(map(str, list_of_ints)))

    print("end of parseLine")


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
                print("\n( ", proxy, " )")
            try:
                scraper = cloudscraper.create_scraper()
                response = scraper.get(i, proxies={"http": proxy, "https": proxy}, headers={'User-Agent': ua.random}, timeout=5)
                time.sleep(random.randrange(1,4))
                lock = 1
                soup = bs4.BeautifulSoup(response.text, 'html.parser')
                tr_box = soup.find_all("tr")
                for l in tr_box:
                    parseLine(l)

                print("-> work in progress (There are ", len(pages), " pages left to analyze.)")
                pages.remove(i)
            except:
                lock = 0
                print(" - fail")

    return df

def scrapper(token, proxies, nbrpages, jump):
    pages = get_pages(token, nbrpages, jump)
    return get_data(pages,proxies)

def launcher(proxies):
    token1 = ["https://hidemy.name/en/proxy-list/?start=", 1280, 64] ###CLOUDFLARE PROTECTION###
    token2 = ["https://www.ip-adress.com/proxy-list", 1, 1]
    token3 = ["http://free-proxy.cz/en/proxylist/main/", 150, 1] ###CAPTCHAT###
    tokens = [token1]
    for tok in range(0, len(tokens)):
        scrapper(tokens[tok][0], proxies, tokens[tok][1], tokens[tok][2])

def main():
    proxies = pd.read_csv('Proxy_List.txt', header = None)
    proxies = proxies.values.tolist()
    proxies = list(it.chain.from_iterable(proxies))

    print("Scraproxy is starting")
    launcher(proxies)
    print("Scraproxy's over")

if __name__== "__main__":
  main()

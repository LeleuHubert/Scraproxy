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
            try:
                scraper = cloudscraper.create_scraper()
                response = scraper.get(i,proxies={"http": proxy, "https": proxy}, headers={'User-Agent': ua.random},timeout=5)
                time.sleep(random.randrange(1,4))
                lock = 1

                soup = bs4.BeautifulSoup(response.text, 'html.parser')
                tr_box = soup.find_all("tr")

                for par in param:
                    l = []
                    for el in tr_box:
                        j = el[par]
                        l.append(j)
                    l = pd.DataFrame(l, columns = [par])
                    df_f = pd.concat([df_f,l], axis = 1)
                df = df.append(df_f, ignore_index=True)

                print(df.shape, " ( ", proxy, " )")
                pages.remove(i)
            except:
                print("TIME OUT : ", proxy, " url : ", i)
                lock = 0

    return df

def scrapper(token, proxies, nbrpages, jump):
    pages = get_pages(token, nbrpages, jump)
    return get_data(pages,proxies)

def launcher(proxies):
    token1 = ["https://hidemy.name/en/proxy-list/?start=", 1280, 64] ###CLOUDFLARE PROTECTION###
    token2 = ["https://www.ip-adress.com/proxy-list", 1, 1]
    token3 = ["http://free-proxy.cz/en/proxylist/main/", 150, 1] ###CAPTCHAT###
    tokens = [token1]
    for tok in range(0, len(tokens)+1):
        scrapper(tokens[tok][0], proxies, tokens[tok][1], tokens[tok][2]).to_csv(r'list.csv', index = False, header=True)
    print("the file 'list.csv' was created")

def main():
    proxies = pd.read_csv('Proxy_List.txt', header = None)
    proxies = proxies.values.tolist()
    proxies = list(it.chain.from_iterable(proxies))

    print("Scraproxy is starting")
    launcher(proxies)
    print("Scraproxy's over")

if __name__== "__main__":
  main()

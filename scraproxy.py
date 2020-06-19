import pandas as pd
import time
import bs4
import random
import requests
from fake_useragent import UserAgent
import itertools as it

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
                response = requests.get(i,proxies={"http": proxy, "https": proxy}, headers={'User-Agent': ua.random},timeout=5)
                time.sleep(random.randrange(1,4))
                lock = 1

                soup = bs4.BeautifulSoup(response.text, 'html.parser')
                tr_box = soup.find_all("tr")
                print("PROXY OK : élément decouvert ", len(tr_box))
                print(tr_box)
                pages.remove(i)
            except:
                print("TIME OUT : ", proxy, " url : ", i)
                lock = 0

    return df

def scrapper(token, proxies, nbrpages, jump):
    pages = get_pages(token, nbrpages, jump)
    return get_data(pages,proxies)

def launcher(proxies):
    token1 = ["https://www.ip-adress.com/proxy-list", 1, 1]
    token2 = ["https://hidemy.name/en/proxy-list/?start=", 1280, 64] ###CLOUDFLARE PROTECTION###
    token3 = ["http://free-proxy.cz/en/proxylist/main/", 150, 1] ###CAPTCHAT###
    tokens = [token1, token2, token3]

    for tok in range(0, len(tokens)+1):
        scrapper(tokens[tok][0], proxies, tokens[tok][1], tokens[tok][2]).to_csv(r'list.csv', index = False, header=True)


def main():
    proxies = pd.read_csv('Proxy_List.txt', header = None)
    proxies = proxies.values.tolist()
    proxies = list(it.chain.from_iterable(proxies))

    print("Scraproxy is starting")
    launcher(proxies)
    print("Scraproxy's over")



if __name__== "__main__":
  main()

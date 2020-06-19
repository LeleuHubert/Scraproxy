import pandas as pd
import time
import bs4
import random
import requests
from fake_useragent import UserAgent
import itertools as it

def get_pages(token, nb):
    pages = []
    for i in range(1, nb+1, 64):
        j = token + str(i)
        pages.append(j)
    print("detection de", len(pages), " pages")
    return pages

def get_data(pages,proxies):

    df = pd.DataFrame()
    parameters = ['tr']
    ua = UserAgent()
    proxy_pool = it.cycle(proxies)
    lock = 0

    while len(pages) > 0:
        for i in pages:
            df_f = pd.DataFrame()
            if lock == 0:
                proxy = next(proxy_pool)
            try:
                response = requests.get(i,proxies={"http": proxy, "https": proxy}, headers={'User-Agent': ua.random},timeout=5)
                time.sleep(random.randrange(1,4))
                print("[ ", i, " ] -> ", proxy)
                lock = 1


            except:
                print("ERROR : [ ", i, " ] - ", proxy, " time out" )
                lock = 0

    return df

token = 'https://hidemy.name/en/proxy-list/?start='
pages = get_pages(token,1280)
proxies = pd.read_csv('Proxy_List.txt', header = None)
proxies = proxies.values.tolist()
proxies = list(it.chain.from_iterable(proxies))
data = get_data(pages,proxies)

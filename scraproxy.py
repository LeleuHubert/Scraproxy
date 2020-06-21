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
    stock = []
    pattern = ["\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "^(6553[0-5]|655[0-2]\d|65[0-4]\d\d|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0)$ "] #ip, port

    for elem in line:
        for pat in pattern:
            result = re.match(pat, elem)
            if result:
                stock.append(result)

    with open('list.csv', 'a') as f:
        writer = csv.writer(f)
        for cell in stock:
            writer.writerows(cell)

def connector(i, proxy, ua):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(i, proxies={"http": proxy, "https": proxy}, headers={'User-Agent': ua.random}, timeout=5)
    time.sleep(random.randrange(1,4))
    print("- step n°1 done [connector]")
    return bs4.BeautifulSoup(response.text, 'html.parser')

def get_data(pages, proxies, pattern):
    df = pd.DataFrame()
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
                tr_box = soup.find_all(pattern[0], {"class":pattern[1]})

                if len(tr_box) != 0:
                    for l in tr_box:
                        parseLine(l)
                    print("- step n°2 done [parseLine]")

                print("- step n°3 done [get_data]")
                print("### ", len(pages), " pages left ###")
                pages.remove(i)

            except:
                print("- Proxy time out")
                lock = 0

    return df

def launcher(proxies):
    token0 = ["http://nntime.com/proxy-list-", 7, 1, 1, ["tr", "odd"]]
    token1 = ["http://nntime.com/proxy-list-", 7, 1, 1, ["tr", "even"]]

    token2 = ["https://hidemy.name/fr/proxy-list/?start=", 1280, 64, 0, ["tr",""]] ###CLOUDFLARE PROTECTION###
    token3 = ["https://www.ip-adress.com/proxy-list", 1, 1, 0, ["tr",""]]
    token4 = ["http://free-proxy.cz/en/proxylist/main/", 150, 1, 0, ["tr",""]] ###CAPTCHAT###

    tokens = [token0, token1]
    for tok in tokens:
        get_data(get_pages(tok), proxies, tok[4])

def main():
    proxies = pd.read_csv('Proxy_List.txt', header = None)
    proxies = proxies.values.tolist()
    proxies = list(it.chain.from_iterable(proxies))

    print("Scraproxy is starting")
    launcher(proxies)
    print("Scraproxy's over")

if __name__== "__main__":
  main()

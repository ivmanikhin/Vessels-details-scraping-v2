import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re


def get_cnos_batch(pagenum):
    url = "https://www.ccs.org.cn/ccswzen/internationalShipsList"
    querystring = {"columnid":"201900002000000123","currentPage":str(pagenum)}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.ccs.org.cn/ccswzen/internationalShipsList?columnid=201900002000000123",
        "Cookie": "JSESSIONID=FA6360C39AFAC2A8A53EADB8603B8635",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1"
    }
    for attempt in range(10):
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            print("Got response")
            break
        except:
            print("Something went wrong\nRetrying...")
    soup = bs(response.text, 'html.parser')
    cnos_batch_raw = soup.select('td[data-title="Ship registration number"]')
    cnos_batch = [cno.button.font.text for cno in cnos_batch_raw]
    print(cnos_batch)
    return cnos_batch


def get_all_cnos(first_page=1, last_page=279):
    all_cnos = []
    for page_num in range(first_page, last_page+1):
        all_cnos += get_cnos_batch(page_num)
        print(f"Got total {len(all_cnos)} CNOs")
    return all_cnos


def get_ship_details(cno):
    url = "https://www.ccs.org.cn/ccswzen/internationalShipDetail"
    querystring = {"ccsno": str(cno)}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.ccs.org.cn/ccswzen/internationalShipsList?columnid=201900002000000123",
        "Cookie": "JSESSIONID=FA6360C39AFAC2A8A53EADB8603B8635",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    soup = bs(response.text, "lxml")
    table_headings = soup.find_all("th")
    table_values = soup.find_all("td")
    for _ in range(len(table_headings)):
        table_headings[_] = " ".join(table_headings[_].text.strip().splitlines())
        table_values[_] = table_values[_].text.strip()
    ship_details = pd.DataFrame([table_values], columns=table_headings)
    return ship_details


def parse_list(cnos_batch):
    ships_details_df = pd.DataFrame()
    for cno in cnos_batch:
        ships_details_df = ships_details_df.append(get_ship_details(cno), ignore_index=True)
        print(ships_details_df.shape)
    return ships_details_df



#re.findall("([\dA-Za-z]{7})", cno.text)[0]
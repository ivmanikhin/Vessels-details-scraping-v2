import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep
import httpx
import asyncio
import os

SEP = os.sep

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://irclass.org/shipsearch',
    'Connection': 'keep-alive',
    'Cookie': '__utma=156765667.1835168435.1641867555.1641867555.1641867555.1; __utmb=156765667.3.10.1641867555; __utmc=156765667; __utmz=156765667.1641867555.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _ga=GA1.2.1835168435.1641867555; _gid=GA1.2.457355012.1641867555',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin'
}

REPLACE_CHARS = str.maketrans({
    " ": "_",
    "(": "",
    ")": "",
})


results = pd.DataFrame()


async def log_request(request):
    print(f"Request: {request.method} {request.url}")


async def log_response(response):
    request = response.request
    print(f"Request: {request.method} {request.url} - Status {response.status_code}")


async def get_ship_details(cno):
    global results
    async with httpx.AsyncClient(event_hooks={'request': [log_request], 'response': [log_response]}) as client:
        url = f"https://irclass.org/umbraco/Surface/Home/_ShipSearchDetail/{cno}"
        response = await client.get(url, headers=HEADERS, timeout=60)
        try:
            soup = bs(response.text, "lxml")
            table_headers = [" ".join(_.text.split()) for _ in soup.find_all("td")[::2]]
            table_values = [" ".join(_.text.split()) for _ in soup.find_all("td")[1::2]]
            ship_details = pd.DataFrame([table_values], columns=table_headers)
            col_names = pd.Series([column.lower().translate(REPLACE_CHARS) for column in ship_details.columns])
            for _ in ship_details.columns[ship_details.columns.duplicated(keep=False)]:
                col_names[ship_details.columns.get_loc(_)] = ([_ + '_' + str(d_idx) if d_idx != 0 else _
                                                     for d_idx in range(ship_details.columns.get_loc(_).sum())])
            ship_details.columns = col_names
            results = results.append(ship_details, ignore_index=True)
        except:
            pass
        return


async def parse_cnos_list(cnos):
    tasks = []
    for cno in cnos:
        tasks.append(get_ship_details(cno))
    await asyncio.gather(*tasks)


# def parse_list(cnos_batch):
#     ships_details_df = pd.DataFrame()
#     for cno in cnos_batch:
#         ships_details_df = ships_details_df.append(get_ship_details(cno), ignore_index=True)
#         print(ships_details_df.shape)
#     return ships_details_df


def read_cnos_from_xlsx():
    regbook = pd.read_excel(f"IRS_parser{SEP}ger_book.xlsx")
    cnos = regbook['IR Number'].to_list()
    return cnos

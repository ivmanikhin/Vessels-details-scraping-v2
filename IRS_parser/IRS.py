import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep


def get_ship_details(cno_and_delay):
    if isinstance(cno_and_delay, tuple):
        cno = cno_and_delay[0]
        delay = cno_and_delay[1]
    else:
        cno = cno_and_delay
        delay = 0
    url = f"https://irclass.org/umbraco/Surface/Home/_ShipSearchDetail/{cno}"
    headers = {
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
    sleep(delay)
    for attempt in range(50):
        try:
            response = requests.request("GET", url, headers=headers, timeout=5)
            break
        except:
            if attempt < 49:
                print(f"Something goes wrong\nRetrying... Attemp {attempt + 1}")
    soup = bs(response.text, "lxml")
    table_headers = [" ".join(_.text.split()) for _ in soup.find_all("td")[::2]]
    table_values = [" ".join(_.text.split()) for _ in soup.find_all("td")[1::2]]
    ship_details = pd.DataFrame([table_values], columns=table_headers)
    col_names = pd.Series(ship_details.columns)
    for _ in ship_details.columns[ship_details.columns.duplicated(keep=False)]:
        col_names[ship_details.columns.get_loc(_)] = ([_ + '_' + str(d_idx) if d_idx != 0 else _
                                             for d_idx in range(ship_details.columns.get_loc(_).sum())])
    ship_details.columns = col_names
    return ship_details


def parse_list(cnos_batch):
    ships_details_df = pd.DataFrame()
    for cno in cnos_batch:
        ships_details_df = ships_details_df.append(get_ship_details(cno), ignore_index=True)
        print(ships_details_df.shape)
    return ships_details_df


def read_cnos_from_xlsx():
    regbook = pd.read_excel("IRS_parser\ger_book.xlsx")
    cnos = regbook['IR Number'].to_list()
    return cnos

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_ship_details(cno):
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
    for attemp in range(50):
        try:
            response = requests.request("GET", url, headers=headers, timeout=5)
            break
        except:
            if attemp < 49:
                print(f"Something goes wrong\nRetrying... Attemp {attemp+1}")
    soup = bs(response.text, "lxml")
    table_headers = soup.find_all("td")[::2]
    table_values = soup.find_all("td")[1::2]
    ship_details = pd.DataFrame(table_values, columns=table_headers)
    return ship_details

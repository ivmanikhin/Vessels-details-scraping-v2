import requests


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

    response = requests.request("GET", url, headers=headers)

    print(response.text)

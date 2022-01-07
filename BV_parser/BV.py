from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import BV_parser.constants as consts
import re
import pandas as pd
import time
import requests
import http.client
import json
import traceback


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")


def get_cnos_list(pagenum, pagesize=5000):
    conn = http.client.HTTPSConnection("marine-offshore.bureauveritas.com")

    payload = '{"draw":' + str(pagenum) + ',"columns":[{"data":"ship_name","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"register_number","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"imo_number","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}}],"order":[{"column":0,"dir":"asc"}],"start":' + str(pagesize * (pagenum - 1)) + ',"length":' + str(pagesize) + ',"search":{"value":"","regex":false},"searchData":{"multiSearchValue":[],"searchValue":"","isContains":true,"isEqualsTo":false,"isStartwith":false,"isIncludeexnames":true},"advanceSearchData":{},"hullSearchData":{}}'

    headers = {
        'POST /bv-fleet/bv-fleet-api/ship/search/basic HTTP/1.1': "",
        'Host': "marine-offshore.bureauveritas.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        'Accept': "application/json, text/plain, */*",
        'Accept-Language': "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        'Accept-Encoding': "gzip, deflate, br",
        'x-api-key': "56db877b-af84-47c0-9ed5-84134a9d91d2",
        'Content-Type': "application/json",
        'Content-Length': str(len(payload)),
        'Origin': "https://marine-offshore.bureauveritas.com",
        'Connection': "keep-alive",
        'Referer': "https://marine-offshore.bureauveritas.com/bv-fleet/",
        'Cookie': "cookie-agreed=2; cookie-agreed-categories=[\"necessary\"]; cookie-agreed-version=1.0.0",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin",
        'Sec-GPC': "1"
    }

    conn.request("POST", "/bv-fleet/bv-fleet-api/ship/search/basic", payload, headers)

    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    cnos = [item["registerNumber"] for item in data["data"]]
    return cnos


def parse_list(cno_list):
    dataset = []
    for cno in cno_list:
        try:
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
                'Accept': "application/json, text/plain, */*",
                'Accept-Language': "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                'Accept-Encoding': "gzip, deflate, br",
                'x-api-key': "56db877b-af84-47c0-9ed5-84134a9d91d2",
                'Connection': "keep-alive",
                'Referer': "https://marine-offshore.bureauveritas.com/bv-fleet/",
                'Cookie': "cookie-agreed=2; cookie-agreed-categories=[necessary]; cookie-agreed-version=1.0.0",
                'Sec-Fetch-Dest': "empty",
                'Sec-Fetch-Mode': "cors",
                'Sec-Fetch-Site': "same-origin",
                'Sec-GPC': "1",
                'TE': "trailers"
            }
            req = requests.get(
                f"https://marine-offshore.bureauveritas.com/bv-fleet/bv-fleet-api/wrapper/ship/particulars/{cno}",
                headers=headers)
            data = req.json()
            # replce lists in json by strings:
            for key in data.keys():
                data[key] = "; ".join(data[key]) if isinstance(data[key], list) else data[key]
            dataset.append(data)
            print(pd.DataFrame(dataset).tail(1))
        except:
            traceback.print_exc()
            pass
    return pd.DataFrame(dataset)


class BV(webdriver.Chrome):
    def __init__(self, driver_path=consts.DRIVER_PATH, teardown=False):
        super(BV, self).__init__(executable_path=driver_path, options=chrome_options)
        self.implicitly_wait(5)
        self.teardown = teardown

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_search_page(self):
        self.get(consts.URL)
        self.switch_to.window(self.window_handles[0])
        time.sleep(1)
        cookies_btn = WebDriverWait(self, 5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[class='eu-cookie-compliance-save-preferences-button accept-selection-button']")))
        cookies_btn.click()
        print("Search page has loaded")

    def get_cno_list(self, search_text):
        search_input_box = self.find_element(By.ID, value="searchValue")
        search_input_box.send_keys(search_text, Keys.RETURN)
        items_per_page_50 = self.find_element(By.CSS_SELECTOR, value="label[for='item-50']")
        items_per_page_50.click()
        # WebDriverWait(self, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'strong[_ngcontent-c1=""]')))
        cno_list = []
        while True:
            time.sleep(3)
            links_table = self.find_element(By.CSS_SELECTOR, value='ul[class="list-requests-certificates js-has-toggle-view view-grid"]')
            ship_cards = links_table.find_elements(By.CSS_SELECTOR, value='div[class="teaser-request-certificate default"]')
            for ship_card in ship_cards:
                cno = re.findall(r"\b([\dA-Z]{6})\b", ship_card.text)[0]
                cno_list.append(cno)
                print(cno)
            print(f"Got {len(cno_list)} CNOs")
            try:
                next_page = self.find_element(By.CSS_SELECTOR, value='a[title="Go to next page"]')
                next_page.click()
            except:
                break
        return cno_list




        # search_button = self.find_element(By.CLASS_NAME, value="button-action small")
        # search_button.click()
        # cno_list = []

    # def get_ship_details(self):
    #     table = self.find_element(By.CSS_SELECTOR, value='app-ship-details[]').get_attribute('outerHTML')
    #     print(table)
    #     df = pd.read_html(table)[0].transpose()
    #     df.dropna(how='all', axis=0, inplace=True)
    #     df.dropna(how='all', axis=1, inplace=True)
    #     df.columns = df.iloc[0]
    #     df.columns = df.columns.str.replace(' :', '').str.replace('&', 'and')
    #     # Rename columns with duplicated names:
    #     col_names = pd.Series(df.columns)
    #     for _ in df.columns[df.columns.duplicated(keep=False)]:
    #         col_names[df.columns.get_loc(_)] = ([_ + '_' + str(d_idx) if d_idx != 0 else _
    #                                              for d_idx in range(df.columns.get_loc(_).sum())])
    #     df.columns = col_names
    #     df = df[1:]
    #     df.reset_index(drop=True, inplace=True)
    #     print(df)
    #     return df
    #
    # def parse_page(self):
    #     df = pd.DataFrame()
    #     while True:
    #         try:
    #             ship_details_buttons = self.find_elements(By.CSS_SELECTOR, value="a[class='img-action small open-popin-survey-address']")
    #             for button in ship_details_buttons:
    #                 button.click()
    #                 time.sleep(1)
    #                 df.append(self.get_ship_details(), ignore_index=True)
    #                 self.find_element(By.CSS_SELECTOR, value="div[class='greybox--close']").click()
    #         except:
    #             pass

        # next_page = self.find_element(By.CSS_SELECTOR, value="a[title='Go to last page']")
        # next_page.click()
        # self.find_element(by="id", value="LinkButton_Search").click()
        # while True:
        #     try:
        #         cno_find_in = self.find_element(by="id", value="result").get_attribute('outerHTML')
        #         cno_list += re.findall("goone\(&quot;(\d+)&quot;\)", cno_find_in)
        #         print(len(cno_list))
        #         next_page = self.find_element(By.LINK_TEXT, value="-[Next]").get_attribute("href")
        #         self.execute_script(next_page)
        #     except:
        #         break
        # self.quit()
        # return cno_list




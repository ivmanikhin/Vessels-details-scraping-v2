from selenium.webdriver.common.by import By
from selenium import webdriver
import NKK_parser.constants as consts
import re
import pandas as pd


class NKK(webdriver.Chrome):
    def __init__(self, driver_path=consts.DRIVER_PATH):
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)
        pd.set_option("display.max_rows", None)
        pd.set_option('max_colwidth', None)
        super(NKK, self).__init__(executable_path=driver_path)
        self.implicitly_wait(15)

    def land_first_page(self):
        self.get(consts.URL)
        self.switch_to.window(self.window_handles[0])

    def get_links_list(self):
        cno_list = []
        self.find_element(by="id", value="LinkButton_Search").click()
        while True:
            try:
                cno_find_in = self.find_element(by="id", value="result").get_attribute('outerHTML')
                cno_list += re.findall("goone\(&quot;(\d+)&quot;\)", cno_find_in)
                print(len(cno_list))
                next_page = self.find_element(By.LINK_TEXT, value="-[Next]").get_attribute("href")
                self.execute_script(next_page)
            except:
                break
        self.quit()
        return cno_list

    def land_links_page(self):
        self.get(consts.URL)
        self.switch_to.window(self.window_handles[0])
        self.find_element(by="id", value="LinkButton_Search").click()

    def get_ship_details(self, cno):
        self.execute_script(f'goone("{str(cno)}")')
        self.switch_to.window(self.window_handles[1])
        table = self.find_element(by="xpath", value=r'/html/body/div/div/div[1]/div[3]/table').get_attribute(
            'outerHTML')
        df = pd.read_html(table)[0].transpose()
        df.dropna(how='all', axis=0, inplace=True)
        df.dropna(how='all', axis=1, inplace=True)
        df.columns = df.iloc[0]
        df.columns = df.columns.str.replace(' :', '').str.replace('&', 'and')
        # Rename columns with duplicated names:
        col_names = pd.Series(df.columns)
        for _ in df.columns[df.columns.duplicated(keep=False)]:
            col_names[df.columns.get_loc(_)] = ([_ + '_' + str(d_idx) if d_idx != 0 else _
                                                 for d_idx in range(df.columns.get_loc(_).sum())])
        df.columns = col_names
        df = df[1:]
        df.reset_index(drop=True, inplace=True)
        self.switch_to.window(self.window_handles[0])
        return df

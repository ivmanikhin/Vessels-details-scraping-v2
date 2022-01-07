import LRS_parser.constants as consts
import re
import pandas as pd
import time
import requests
import http.client
import json
import traceback
from selenium.webdriver.common.by import By
from selenium import webdriver


def get_cnos_batch(word, pagenum):
    url = "https://www.lr.org/webapi/searchproxy/search"

    payload = {
        "query": {},
        "contentID": "477a4dde-381d-46fc-b1b8-e2ad75fb1d3b",
        "page": pagenum,
        "facets": {
            "lrClassStatus": None,
            "shipType": None,
            "registeredOwner": None,
            "flag": [word]
        },
        "orderby": None
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.lr.org/en/lrofships/",
        "Content-Type": "application/json",
        "Origin": "https://www.lr.org",
        "Connection": "keep-alive",
        "Cookie": "ASP.NET_SessionId=wqln2co12ryhixikgsw4hrh0; ARRAffinity=dd4ec869249e3d9566ca786d6cbf7afd7f6d9716031ffd176919145cecc852ea; ARRAffinitySameSite=dd4ec869249e3d9566ca786d6cbf7afd7f6d9716031ffd176919145cecc852ea; ai_user=v4TrV|2021-12-28T02:32:36.690Z; ai_session=xFXpW|1640658756783|1640658756783; OptanonConsent=isIABGlobal=false&datestamp=Tue+Dec+28+2021+05%3A32%3A38+GMT%2B0300+(%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=5.13.0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&hosts=; OptanonAlertBoxClosed=2021-12-28T02:32:38.754Z",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "TE": "trailers"
    }

    response = requests.request("POST", url, json=payload, headers=headers).json()
    raw_cnos = response["results"]
    cnos = []
    for cno in raw_cnos:
        cnos.append(cno["mastAssetId"])
    return cnos


def get_cnos_list(word_list=consts.FLAGS_LIST):
    cnos_list = []
    for word in word_list:
        pagenum = 0
        cnos_batch = []
        while True:
            pagenum +=1
            cnos_batch_from_page = get_cnos_batch(word, pagenum)
            print(cnos_batch_from_page)
            cnos_batch += cnos_batch_from_page
            if len(cnos_batch_from_page) == 0:
                print(cnos_batch)
                print(f"There are {len(cnos_batch)} results for \"{word}\"")
                break
        cnos_list += cnos_batch
    print(f"{len(cnos_list)} results with duplicates")
    cnos_list = list(set(cnos_list))
    print(f"{len(cnos_list)} results without duplicates")
    return cnos_list


# TODO 2: Make a dataframe from json
def parse_list(cno_list):
    dataset = []
    for cno in cno_list:
        try:
            url = f"https://classdirect.lr.org/api/v1/assets/LRV{cno}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "X-XSRF-TOKEN": "0e4c5d4d-25b1-4367-b164-b02395de2d79",
                "Connection": "keep-alive",
                "Referer": "https://classdirect.lr.org/assets/LRV44413/details",
                "Cookie": "XSRF-TOKEN=0e4c5d4d-25b1-4367-b164-b02395de2d79; mod_auth_openidc_state_NIcMcgYxCMlml_1Yg0miaLu839M=eyJhbGciOiAiZGlyIiwgImVuYyI6ICJBMjU2R0NNIn0..Yia3Tk-xZzv_po-S.Ai9RRAVcbImnM8Dajuo1Y7P90vIO2pWL4yAcZusCxzitOx-w4bKbp-LTMy5v6A8Xhlis6RWPG3AU1gW4lDIaSIC6ME12Yo27VWYAGX8ORkL-aOp3i4YPzf3a_ciCgB_cqjQhr8DCC2clIOCSuZMKJMjccirBZvW6ii97zxWMqz8PLNAmKeRRBUXoDNU2PNaWMahse5CNGMxlCb2JBD_aX4hvpNIXbgEa27054UmrChkdngnV8UR3LcQ_KUZtHdEglPebbmTD1KT2QY3N1HHh9FBpNU46-It50vnlIM1IJ9auveKB-SHtOvU2Mx9M-SRlsPoUHU-X2fU4lRnyAtWpCs1H7_3CYiLSoAALyERffayU9tEpRfnuUNg4b4UKmMPtXcq8Ae-M_9AQlnTFONxqwF4pwwhy5rG2tKbPYNTjCfqxpRDLS2ugtQjuJBS7ifD690henQBGryAmYYjjQwGD_b2mz_IOnn0-gX5swGKJo392GRfDCu9SehVUz05986xXSkS5onPhYtxvRPA3WffSN76web-S4F31KaHdMYW8Dg-pC5ygyY5OvfXpeglk_ZniCDZ3U-WQ79agArz_Vw.G8SX6Uv1X4Ns4iqEjWtfZA; mod_auth_openidc_state_ToT0vmyzFBCZHxcSXDGDlAeSlSc=eyJhbGciOiAiZGlyIiwgImVuYyI6ICJBMjU2R0NNIn0..zEf02V1pVXA8fw3b.mICxRQl3Zj1S6zEYJtSE8bdngC0grsBOUKYnk9Spjj7hudAaI05_vWs6uhHA6IiA4l1T0dAmWhFr8_S1paGO69CXdWfMwUb0gTbAAbiYx0BVAgHySHfCw0X7GLvWz-qZfT7DutW6lwolSXp2iSIrEzPmMLsCxUTEBCGbkOU_yr8zM4KymkNuSjHDMp4iL2YLJ12KY48CciWd--TsGwtQvLy69ewLz2jm4xgFeJhvGnEG41hsXgsT3CiQFPZGc7R1SuDiyCG46x62z3GrtH0WXIIIaHlSJSft5zTd6wzmTzUyC-x5L0PCAzlYd2_g9AHlYWh5MGkV0dwlX4u05RGgRA1avENHqJfB24LRoBhKIZV5xjyB49JYDTQmpm-N4aRFT7rSOaKd8kaId0fjjEw1j1OVWCHD8oMuhjNq_IIsnDPPbM4L1zlCKVv0r3j7ik1yM5P2ykQdjyR_3OUinFIfbK-LwCI21qO9eUWUXU5RH_W_WtWI_nd7btM9FYmFKcoM-hW-Aab6sSUrdIgdavI9dlwraKZOWQKf5dtfP_JqYTQl-1Z5LPhscZjMLUQYmNm-QMpKqBZtWh4pXOFRtg.ywKXHd-Q1RkfBhXS7kdsvg; role=LWPgQg9BZc6XaKWYzvgV_w",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-GPC": "1",
                "TE": "trailers"
            }
            response = requests.request("GET", url, headers=headers).json()
            data = {}
            data.update({"IMO": response["imoNumber"],
                         "ClassNotation": response["classNotation"],
                         "CNO": response["allVersions"][-1]["id"],
                         "Name": response["allVersions"][-1]["name"],
                         })

            url = f"https://classdirect.lr.org/api/v1/assets/LRV{cno}/details"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "X-XSRF-TOKEN": "672ee892-14f5-42db-be17-66ad9b2f17b4",
                "Connection": "keep-alive",
                "Referer": "https://classdirect.lr.org/assets/LRV24063/details",
                "Cookie": "XSRF-TOKEN=672ee892-14f5-42db-be17-66ad9b2f17b4; mod_auth_openidc_state_nJ1b-Vw_DVVOcdiB22lsbdlJ47Q=eyJhbGciOiAiZGlyIiwgImVuYyI6ICJBMjU2R0NNIn0..C07uiT_j0gbzyzh1.V90sRTPhr8k9g50pYdXkOBR5dzRXLKW0srlH3JyXFwQdrAtMSYsyLLWB74l-Cmc-jCUn-HNsP2-Zs4OCxXVWHKqKF5tCkurtlA8l9UwDaAu2jOBxe_EPptoSAa_W0h-xKv1mH2m13RTVAAJIQCCLyb0QdS8Bi4Qu4y2LTB7jw7lzppmKt8BJmXaSaxhkZg0-4e2z2e-C8jZ0WE1O8mUoA6f96JuX_lUfkXlVEpbOj9pQ1rmAcT5XDL7ep6XNHD-mrSm_wtvGM8yiDHgdUWBl_nxj-UcaxR6PaKZ_SCNnvhNGDOfqrRZ9eXddM6fNGxPM6FNi0HTxCUbncuijfzuteR_CDDgAvb6yaJ-g9pVZDhIY850rla1_jlzH4aViOTNfA4v8ykh8JHgs0pnBGHterLs41Lv2sFeFRsvlBFC55GSVt5bsZx0Lx6MfQNNSaOw9gvSx-Zv1PVtgbcqX7xFDBNNa8i6dWDvXQq-Wwi2hVo9DTd-JiaPeEr6ubBbswUMY24zEcR_DFwV8nSfJJ3a-3EC4t8NfkvoCPtvys3B8NBogUpZ_Gea51hgvzgxdZq7yONR7Io5BygsTYwZVtg.J709knlH0k94ADNDsu1xFg; mod_auth_openidc_state_I-pNo3o8vlHjoHgNr5Yo-gQhXP0=eyJhbGciOiAiZGlyIiwgImVuYyI6ICJBMjU2R0NNIn0..-1tlRaszm7RPGYiG.ZaTi-B2DhkMfsj7hMdINTPPPEN2Ka3vU4pN96Vrg_G8oTkl9PSL4C3re1mTxevDH8KDXD45h9UUfwwwt5EAGiZr9GaB2meX0rdoE0cr-2qT10wb7h7UKSXHEg1AmHQa8p8OVa3s_wftvnS4kMGB2ILxKHLPx6VmGdn6EkFgoFLE3rN1wsjG5nElIo7Lc9DO43JAWP9gM2YTIrZTw94MNJwj8lWM5xQvIl06OJAxj3oWA9NshIixf5q0zLWLwgrq0tUZrCvnE-FG39WvSZMkMW3tv4vm_cahcE-uYXyF-R-QMIABRpiCPnhoTyfuTK8WLwFcm71d1mCJ25bHXHSLEQU4Fr-6CByYih8Ptl2EuTdWGDXhyzOlxYQY2x8-oxBLxizDQECufU-p7icCSs1sEwOhKN-a6Tknw9m8pJ8bmEl0UvPZpWxcnUwVK6XsO-l051nNVUjcbTPcW1WbHf1ox4GwPFMOkP1oOc1cPTfvTl7Vv5Lwflka7nIKUkKQoTf-DUYY63dZqgYu6dV-nKRFUABr81hNXLYW7JIk8FRcSVrG7LPWimPjZ-6zPb6AEpaeXX-1b0vo6hGLbQ8qMXQ.DXtH_7cbmKY1Lz6TKjAZDA; role=VVp4OlHrmbkm9Zt-Clno5w",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-GPC": "1",
                "TE": "trailers"
            }
            response = requests.request("GET", url, headers=headers).json()
            data.update(response["registryInformation"])
            data.update(response["principalDimension"])
            data.update(response["rulesetDetailsDto"])
            data.update(response["rulesetDetailsDto"])
            try:
                data.update(response["equipmentDetails"])
            except:
                pass
            for key in data.keys():
                try:
                    data[key] = data[key].strip()
                except:
                    pass
            dataset.append(data)
            print(pd.DataFrame(dataset).tail(1))
        except:
            traceback.print_exc()
            pass
    return pd.DataFrame(dataset)


class LRS(webdriver.Chrome):
    def __init__(self, driver_path=consts.DRIVER_PATH):
        super(LRS, self).__init__(executable_path=driver_path)
        self.implicitly_wait(15)

    def land_first_page(self):
        self.get(consts.URL)
        self.switch_to.window(self.window_handles[0])
        self.find_element(By.ID, value="onetrust-accept-btn-handler").click()

    def get_flags_list(self):
        # time.sleep(1)
        flag_popup_menu = self.find_element(By.CSS_SELECTOR, value="select[id='flag']")
        flag_popup_menu.click()
        raw_flags = self.find_elements(By.TAG_NAME, value="option")
        print(len(raw_flags))
        flag_list = []
        for raw_flag in raw_flags[1:]:
            flag_list.append(raw_flag.get_attribute("value"))
        return flag_list



import DNV_parser.constants as consts
import re
import pandas as pd
import time
import requests
import http.client
import json
import traceback


def get_cnos_batch(word):
    url = "https://vesselregister.dnv.com/vesselregister/api/vessel"

    querystring = {"term": word, "includeHistoricalNames": "false", "includeNonClass": "true", "chunkSize": "1000"}

    headers = {
        "cookie": "com.dnvgl.vesselregister.session=id%3De57769a4383c4c839964be28c9d6ee99%26info%3Dsession; TS01335179=01f50e70eaabda3f85c8bcbd5b810716855c0c41a4ab7cae79707a09f231175c13792586627f6f48a8e32be78b2e4569ea9dbd35d4; TS014634ec=01f50e70eaf41d47048cadfd4eaa1b5cc97f3268c53867b3234ac520513d9a955109db7a156ebfbf14b443e60f7201740fcd7a9b5c",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest",
        "x-dtpc": "65`-0e0",
        "Connection": "keep-alive",
        "Cookie": "dtCookie=v_4_srv_65_sn_E1723074171FE4071FAE25915A6EBE20_perc_100000_ol_0_mul_1_app-3Aaf2b7c5d3febd57a_0; TS01335179=01f50e70eaf41d47048cadfd4eaa1b5cc97f3268c53867b3234ac520513d9a955109db7a156ebfbf14b443e60f7201740fcd7a9b5c; TS01a878af=01f50e70eaf41d47048cadfd4eaa1b5cc97f3268c53867b3234ac520513d9a955109db7a156ebfbf14b443e60f7201740fcd7a9b5c; rxVisitor=1640534881037RFV0NHE66S8CHMQH9M8E66BPRJCITHG0; dtPC=65`-0e0; rxvt=1640536708152|1640534881044; dtLatC=7; dtSa=-",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1"
    }

    response = pd.DataFrame(requests.request("GET", url, headers=headers, params=querystring).json()["Vessels"])
    cnos = response["Id"].to_list()
    return cnos


def get_cnos_list(word_list=consts.WORD_LIST):
    cnos_list = []
    for word in word_list:
        try:
            cnos_batch = get_cnos_batch(word)
            cnos_list += cnos_batch
            print(cnos_batch)
            print(f"There are {len(cnos_batch)} results for \"{word}\"")
        except:
            print(f"There is no \"{word}\" there.")
            pass
    print(f"{len(cnos_list)} results with duplicates")
    cnos_list = list(set(cnos_list))
    print(f"{len(cnos_list)} results without duplicates")
    return cnos_list


def parse_list(cno_list):
    dataset = []
    for cno in cno_list:
        try:
            url = "https://vesselregister.dnv.com/VesselRegister/api/VesselDetails"
            querystring = {"what": "details", "VesselId": cno, "CallSign": "", "Imo": ""}
            headers = {
                "cookie": "com.dnvgl.vesselregister.session=id%3De57769a4383c4c839964be28c9d6ee99%26info%3Dsession; TS01335179=01f50e70ea3569e488149d151200813fae310ab9d85a31f2f71d99597a2f4b734501a057f620f9c0e3994f6faa0c72df12db9a9d10; TS014634ec=01f50e70eaf41d47048cadfd4eaa1b5cc97f3268c53867b3234ac520513d9a955109db7a156ebfbf14b443e60f7201740fcd7a9b5c",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/json; charset=utf-8",
                "X-Requested-With": "XMLHttpRequest",
                "x-dtpc": "65`-0e0",
                "Connection": "keep-alive",
                "Cookie": "dtCookie=v_4_srv_65_sn_E1723074171FE4071FAE25915A6EBE20_perc_100000_ol_0_mul_1_app-3Aaf2b7c5d3febd57a_0; TS01335179=01f50e70ea3edd4b25d446b5370b23f8f338e23403c1ac6b6b214d680f7dd9d18bf05429e678e9bda9cf9536659fb6e7ae962e98c8; TS01a878af=01f50e70eaf41d47048cadfd4eaa1b5cc97f3268c53867b3234ac520513d9a955109db7a156ebfbf14b443e60f7201740fcd7a9b5c; rxVisitor=1640534881037RFV0NHE66S8CHMQH9M8E66BPRJCITHG0; dtPC=65`-0e0; rxvt=1640537089833|1640534881044; dtLatC=148; dtSa=-; com.dnvgl.vesselregister.session=id=4c74c5c4ba154153a7e2e443af8e17d7&info=session; TS014634ec=01f50e70eaf41d47048cadfd4eaa1b5cc97f3268c53867b3234ac520513d9a955109db7a156ebfbf14b443e60f7201740fcd7a9b5c",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-GPC": "1",
                "Cache-Control": "max-age=0"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            data = response.json()
            # replce lists in json by strings:
            temp = ""
            for item in data["AdditionalPurpose"]:
                temp += f"{item['PurposeName']} ({item['PurposeDescription']})\n"
            data["AdditionalPurpose"] = temp
            data.pop("Certificates", None)
            data.pop("Surveys", None)
            for key in data.keys():
                try:
                    data[key] = "; ".join(data[key]) if isinstance(data[key], list) else data[key]
                except:
                    data[key] = ""
            dataset.append(data)
            print(pd.DataFrame(dataset).tail(1))
        except:
            traceback.print_exc()
            pass
    return pd.DataFrame(dataset)



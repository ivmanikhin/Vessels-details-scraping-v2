import http.client
import json
import httpx
import asyncio

def get_cnos_list():
    conn = http.client.HTTPSConnection("www.eagle.org")

    payload = ""

    headers = {
        'cookie': "PORTALSESSIONID=EexMPThunF8D4d-kZ7hAtrnAoM1-ARfNRziyx8LJyzE4iFHnDjcr!-127428686!-1749509283",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
        'Accept': "application/json, text/plain, */*",
        'Accept-Language': "en-US,en;q=0.5",
        'Accept-Encoding': "gzip, deflate, br",
        'X-XSRF-TOKEN': "undefined",
        'ADRUM': "isAjax:true",
        'Connection': "keep-alive",
        'Referer': "https://www.eagle.org/portal/",
        'Cookie': "PORTALSESSIONID=o41MJFLtL14YI5pRvPeZgz1nN2OcIsN0J7p7Qv_pjukFPOL5XckO!-1749509283!-1978394398;"
                  "intercom-id-i9ip4aa0=a44dc2d6-6baf-41bc-9a25-26571f67d361; intercom-session-i9ip4aa0=;"
                  "wp16130=\"UZUWTDDDDDDHIMTCXXZ-MTMM-XKLM-IVUL-WIZWMTYJJCAMDgNssDLHnsL_hkn\";"
                  "_ce.s=v11.rlc~1641954745168; _gcl_au=1.1.499676301.1641954817;"
                  "_lfa=LF1.1.89443ec32aa40931.1641954642702; _ga=GA1.2.1564775793.1641954818;"
                  "_gid=GA1.2.2010263875.1641954818",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin"
        }

    conn.request("GET", "/portal/absrecord/os/ABSRECORDSEARCH?collectioncount=1&oslc.pageSize=20000&pageno=1&searchAttributes=vessel_name%2C&oslc.searchTerms=%22*%22&_lang=en-EN", payload, headers)

    res = conn.getresponse()
    output = [_["assetnum"] for _ in json.loads(res.read())["member"]]
    return output


async def log_request(request):
    print(f"Request: {request.method} {request.url}")


async def log_response(response):
    request = response.request
    print(f"Request: {request.method} {request.url} - Status {response.status_code}")


async def get_ship_details(cno: str):
    global results
    async with httpx.AsyncClient(event_hooks={'request': [log_request], 'response': [log_response]}) as client:
        url = f"https://www.eagle.org/portal/absrecord/os/ABSRECORDVESSEL?&oslc.where=assetnum=%22{cno}%22&absrecord_search_vw.abs_vesselspec.orderBy=%2Bsection_seq,%2Bdisplaysequence&_lang=en-EN"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-XSRF-TOKEN': 'undefined',
            'Connection': 'keep-alive',
            'Referer': 'https://www.eagle.org/portal/',
            'Cookie': 'PORTALSESSIONID=LfxO10IwA9DU7hSYA1DgZAfntgAh6jBw48S55_5uMX_E16WXRFmr!-1749509283!-1978394398; intercom-id-i9ip4aa0=72f0d6c1-a4bb-44e5-8ef7-3495a42a626e; intercom-session-i9ip4aa0=',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1'
        }
        ship_details_r = await client.get(url, headers=headers, timeout=60)
        url = f"https://www.eagle.org/portal/absrecord/script/ABSRECORDCAPACITYSQL?assetnum={cno}&_lang=en-EN"
        headers = {
            "cookie": "PORTALSESSIONID=GjdrErktlR7DyKNpV3zsp5HYcJ_qAreHf1hyEIIHPc2gkEBbN_ba!-127428686!-1749509283",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-XSRF-TOKEN": "undefined",
            "ADRUM": "isAjax:true",
            "Connection": "keep-alive",
            "Referer": "https://www.eagle.org/portal/",
            "Cookie": "PORTALSESSIONID=H9hj_zZMzq2m8ZmRWWdoD1GPSL680MES68FkCikTmUD-26Sgo_Uq!-1978394398!-243536516; "
                      "intercom-id-i9ip4aa0=a44dc2d6-6baf-41bc-9a25-26571f67d361; intercom-session-i9ip4aa0=; "
                      "wp16130=\"UZUWTDDDDDDHIMTCXXZ - MTMM - XKLM - IVUL - WIZWMTYJJCAMDYJWITVLI - YIWM - XVUC - BWAI - "
                      "VZCBBXCCJHUYDLHnsL_hkn\"; _ce.s=v11.rlc~1642355182661; _gcl_au=1.1.499676301.1641954817; "
                      "_lfa=LF1.1.89443ec32aa40931.1641954642702; _ga=GA1.2.1564775793.1641954818; _gat=1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }
        ship_capacity_r = await client.get(url, headers=headers, timeout=60)
        ship_capacity = ship_capacity_r.json()["member"]
        if len(ship_capacity) == 0:
            ship_capacity = [""]
        data = [ship_details_r.json()["member"][0], ship_capacity]
        data[0]["abs_vesselspec"].pop(1)
        results.append(data)
        return


def raw_data_to_dict(data):
    details = data[0]
    output = {}
    replace_chars = str.maketrans({
        " ": "_",
        "(": "",
        ")": "",
    })
    output["imo_num"] = details["imo_num"]
    output["vessel_name"] = details["vessel_name"]
    output["vessel_type"] = details["vessel_type"]
    output["class_notation"] = " ".join(["".join(["(Malte cross)" if _["maltese_cross"] else "", _["spec"]])
                                         if _["service_type"] == "Class Certification" else ""
                                         for _ in details["abs_service_spec"]])
    output["flag"] = details["flag_name"]
    output["port_registry"] = details["port_registry"]
    output["class_num"] = details["class_num"]
    for _ in details["abs_tonnage"]:
        if _["gross_tonnage"] != 0:
            output["net_tonnage"] = _["net_tonnage"]
            output["gross_tonnage"] = _["gross_tonnage"]
    for _ in details["abs_vesselspec"]:
        output[_["description"].lower().translate(replace_chars)] = _["numvalue"]
    output["marpol_category"] = details["marpol_category"]
    output["solas_category"] = details["solas_category"]
    output["vessel_description"] = details["vessel_description"]
    output["delivery_date"] = details["delivery_date"]
    try:
        output["shipyard"] = details["abs_shipyard_designation"][0]["abs_shipyard_description"]
    except:
        pass
    try:
        output["customer"] = details["abs_customers"][0]["customer_name"]
    except:
        pass

    capacity = data[1]
    if capacity != [""]:
        for category in capacity:
            output[category["category"].lower().translate(replace_chars)] = category["total_volume"]
    return output


async def parse_cnos_list(cnos):
    tasks = []
    for cno in cnos:
        tasks.append(get_ship_details(cno))
    await asyncio.gather(*tasks)


results = []

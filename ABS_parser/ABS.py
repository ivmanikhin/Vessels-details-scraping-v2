import http.client
import json
import aiohttp
import httpx
import asyncio

import httpx


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
        r = await client.get(url, headers=headers)
        data = r.json()["member"][0]
        output = {}
        replace_chars = str.maketrans({
            " ": "_",
            "(": "",
            ")": "",
        })
        output["imo_num"] = data["imo_num"]
        output["vessel_name"] = data["vessel_name"]
        output["vessel_type"] = data["vessel_type"]
        output["class_notation"] = " ".join(["".join(["(Malte cross)" if _["maltese_cross"] else "", _["spec"]])
                                             if _["service_type"] == "Class Certification" else ""
                                             for _ in data["abs_service_spec"]])
        output["flag"] = data["flag_name"]
        output["port_registry"] = data["port_registry"]
        output["class_num"] = data["class_num"]
        for _ in data["abs_tonnage"]:
            if _["gross_tonnage"] != 0:
                output["net_tonnage"] = _["net_tonnage"]
                output["gross_tonnage"] = _["gross_tonnage"]
        data["abs_vesselspec"].pop(1)
        for _ in data["abs_vesselspec"]:
            output[_["description"].lower().translate(replace_chars)] = _["numvalue"]
        output["marpol_category"] = data["marpol_category"]
        output["solas_category"] = data["solas_category"]
        output["vessel_description"] = data["vessel_description"]
        output["delivery_date"] = data["delivery_date"]
        output["shipyard"] = data["abs_shipyard_designation"][0]["abs_shipyard_description"]
        # output["customer"] = data["abs_customers"][0]["customer_name"]
        results.append(output)
        return



# async def get_ship_details(session, cno):
#
#     url = f"https://www.eagle.org/portal/absrecord/os/ABSRECORDVESSEL?&oslc.where=assetnum=%22{cno}%22&absrecord_search_vw.abs_vesselspec.orderBy=%2Bsection_seq,%2Bdisplaysequence&_lang=en-EN"
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
#         'Accept': 'application/json, text/plain, */*',
#         'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'X-XSRF-TOKEN': 'undefined',
#         'Connection': 'keep-alive',
#         'Referer': 'https://www.eagle.org/portal/',
#         'Cookie': 'PORTALSESSIONID=LfxO10IwA9DU7hSYA1DgZAfntgAh6jBw48S55_5uMX_E16WXRFmr!-1749509283!-1978394398; intercom-id-i9ip4aa0=72f0d6c1-a4bb-44e5-8ef7-3495a42a626e; intercom-session-i9ip4aa0=',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-GPC': '1'
#     }
#     async with session.get(url, headers=headers) as res:
#         return await res.text()


async def parse_cnos_list(cnos):
    tasks = []
    for cno in cnos:
        tasks.append(get_ship_details(cno))
    await asyncio.gather(*tasks)

    # ships_details = []
    # for result in data:
    #     data = json.loads(result)["member"][0]
    #     output = {}
    #     replace_chars = str.maketrans({
    #         " ": "_",
    #         "(": "",
    #         ")": "",
    #     })
    #
    #     output["imo_num"] = data["imo_num"]
    #     output["vessel_name"] = data["vessel_name"]
    #     output["vessel_type"] = data["vessel_type"]
    #     output["class_notation"] = " ".join(["".join(["(Malte cross)" if _["maltese_cross"] else "", _["spec"]])
    #                                          if _["service_type"] == "Class Certification" else ""
    #                                          for _ in data["abs_service_spec"]])
    #     output["flag"] = data["flag_name"]
    #     output["port_registry"] = data["port_registry"]
    #     output["class_num"] = data["class_num"]
    #     for _ in data["abs_tonnage"]:
    #         if _["gross_tonnage"] != 0:
    #             output["net_tonnage"] = _["net_tonnage"]
    #             output["gross_tonnage"] = _["gross_tonnage"]
    #     data["abs_vesselspec"].pop(1)
    #     for _ in data["abs_vesselspec"]:
    #         output[_["description"].lower().translate(replace_chars)] = _["numvalue"]
    #     output["marpol_category"] = data["marpol_category"]
    #     output["solas_category"] = data["solas_category"]
    #     output["vessel_description"] = data["vessel_description"]
    #     output["delivery_date"] = data["delivery_date"]
    #     output["shipyard"] = data["abs_shipyard_designation"][0]["abs_shipyard_description"]
    #     # output["customer"] = data["abs_customers"][0]["customer_name"]
    #     ships_details.append(output)
    # return ships_details
results = []

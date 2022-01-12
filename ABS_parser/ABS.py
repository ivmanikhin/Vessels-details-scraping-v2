import http.client
import json


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

    conn.request("GET", "/portal/absrecord/os/ABSRECORDSEARCH?collectioncount=1&oslc.pageSize=100&pageno=1&searchAttributes=vessel_name%2C&oslc.searchTerms=%22*%22&_lang=en-EN", payload, headers)

    res = conn.getresponse()
    data = json.loads(res.read())["member"]
    return data


def get_ship_details(cno):
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
        'Cookie': "PORTALSESSIONID=mn1MNNXQgzRZ1JwosgwRrjVKYv78S8xQFfHQebH5Py4N-HHQBPzX!-127428686!-1749509283;"
                  "intercom-id-i9ip4aa0=a44dc2d6-6baf-41bc-9a25-26571f67d361; intercom-session-i9ip4aa0=;"
                  "wp16130=\"UZUWTDDDDDDHIMTCXXZ - MTMM - XKLM - IVUL - WIZWMTYJJCAMDgNssDLHnsL_hkn\";"
                  "_ce.s=v11.rlc~1641956618770; _gcl_au=1.1.499676301.1641954817;"
                  "_lfa=LF1.1.89443ec32aa40931.1641954642702; _ga=GA1.2.1564775793.1641954818;"
                  "_gid=GA1.2.2010263875.1641954818; _gat=1",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin"
    }

    conn.request("GET",
                 f"/portal/absrecord/os/ABSRECORDVESSEL?oslc.where=assetnum%3D%22{cno}%22&absrecord_search_vw.abs_vesselspec.orderBy=%2Bsection_seq%2C%2Bdisplaysequence&_lang=en-EN",
                 payload, headers)

    res = conn.getresponse()
    data = json.loads(res.read())["member"]
    return data
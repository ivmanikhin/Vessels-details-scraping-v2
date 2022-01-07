import pandas as pd
import sqlite3
import numpy as np
import time
import requests

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_rows", None)

HEADERS = {
    "Host": "marine-offshore.bureauveritas.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Accept": "application/json\", \"text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://marine-offshore.bureauveritas.com/bv-fleet/",
    "x-api-key": "56db877b-af84-47c0-9ed5-84134a9d91d2",
    "Connection": "keep-alive",
    "Cookie": "cookie-agreed=2; cookie-agreed-categories=[\"necessary\",\"analytics\",\"targeting_advertising\"]; cookie-agreed-version=1.0.0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "TE": "trailers",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

data = requests.get(f"https://marine-offshore.bureauveritas.com/bv-fleet/bv-fleet-api/wrapper/ship/particulars/{cno}", headers=HEADERS)
df = pd.json_normalize(data.json())
print(df.transpose())























#
# con = sqlite3.connect('ships_final.db')
# df = pd.read_sql_query("SELECT * FROM ships_details", con=con)
# con.close()
# classes = pd.read_csv("from_iacs.csv", sep=";")
# df["IMO"] = df["Ship name"].str.extract("\((\d\d\d\d\d\d\d)\)")
# df = df.drop(df.index[df[df["IMO"].isna()].index], axis=0)
# df["IMO"] = df["IMO"].astype(np.int32)
# df["Ship name"] = df["Ship name"].str.extract("(.+) \(\d\d\d\d\d\d\d\)")
#
# classes["IMO"] = classes["IMO"].astype(np.int32)
# print(df.head())
# classes = classes.drop_duplicates("IMO", keep="last")
#
# for _ in df.index:
#     if classes["CLASS"][classes["IMO"] == df["IMO"][_]].values:
#         df["Classification"][_] = classes["CLASS"][classes["IMO"] == df["IMO"][_]].values[0]
# print(df.tail())
# for _ in reversed(range(11)):
#     print(_)
#     time.sleep(1)
#
# con = sqlite3.connect('ships_final.db')
# df.to_sql(name="s_details_imo_class", con=con, if_exists="replace", index=False)
# con.close()


# DATA_TYPES = {
#     "int": "Integer",
#     "float": "Real",
#     "str": "Text",
#     "object": "Text"
# }

# con = sqlite3.connect('ships.db')
# spsheet = pd.read_sql_query("SELECT * FROM ships_details WHERE `HFO Consumption`=(SELECT MAX(`HFO Consumption`) FROM ships_details);", con=con)
# con.close()
# spsheet.insert(loc=0, column="Something else", value=12)
# spsheet.insert(loc=1, column="Something else more", value="dsasdf")
#
#
# def new_column_to_sql():
#     for col_name in list(spsheet.columns.values):
#         if col_name not in list(database.columns.values):
#             print(f"New column: \"{col_name}\"")
#             data_type_py = re.search("([a-zA-Z]+)", str(spsheet.dtypes[col_name])).group(1)
#             print(f"Python data type: \"{data_type_py}\"")
#             data_type_sql = DATA_TYPES[data_type_py]
#             print(f"SQL data type: \"{data_type_sql}\"")
#             con = sqlite3.connect("ships_backup.db")
#             cur = con.cursor()
#             cur.execute(f"ALTER TABLE ships_details ADD COLUMN `{col_name}` {data_type_sql}")
#             con.close()
#
# new_column_to_sql()
import numpy as np
import pandas as pd

from ABS_parser import ABS
from tabulate import tabulate
import asyncio
import os
from easy_SQL.easy_SQL import *
import pprint

SEP = os.sep



pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_rows", None)
pd.set_option('max_colwidth', None)

def make_search_list(list_of_something, batch_size=5):
    structured_list = []
    num_of_sublists = int(round(len(list_of_something) / batch_size))
    for i in np.array_split(list_of_something, num_of_sublists):
        structured_list.append(list(i))
    return structured_list


def write_list_to_txt(list_of_something, filename, mode="a"):
    with open(f"{filename}", mode) as f:
        for _ in list_of_something:
            f.write(str(_) + "\n")


def read_txt_to_list(filename):
    output_list = []
    with open(f"{filename}", "r") as f:
        for line in f:
            output_list.append(line.strip())
    return output_list


# cnos_list = read_txt_to_list(f"ABS_parser{SEP}cnos_list.txt")
# print(f"Total {len(cnos_list)} vessels")
# search_list = make_search_list(cnos_list, 100)
# print(f"{len(search_list)} batches with {len(search_list[0])} elements each")
# time.sleep(3)
# i = 0
# for cnos_list in search_list[86:]:
#     i += 1
#     print(f"Batch {i} of {len(search_list)}")
#     time.sleep(2)
#     asyncio.run(ABS.parse_cnos_list(cnos_list))
#     ships_details_batch = []
#     for raw_data in ABS.results:
#         try:
#             ships_details = ABS.raw_data_to_dict(raw_data)
#             ships_details_batch.append(ships_details)
#         except:
#             pass
#     result = pd.DataFrame.from_dict(ships_details_batch)
#     print(tabulate(result, headers='keys', tablefmt='psql'))
#     write_to_sql(result, "ABS_details")
#     ABS.results.clear()

# asyncio.run(ABS.parse_cnos_list(["V0226108"]))
# ships_details_batch = []
# for raw_data in ABS.results:
#     try:
#         ships_details = ABS.raw_data_to_dict(raw_data)
#         ships_details_batch.append(ships_details)
#     except:
#         pass
# result = pd.DataFrame.from_dict(ships_details_batch)
# print(tabulate(result, headers='keys', tablefmt='psql'))
# ABS.results.clear()

result = extract_table_from_sql(table_name="CCS_details", sql_column_names="`Class No.`, `Cylinders,Diameter,Power &Revolution of Main Engine`, `Type of Number of Main Engine`", df_column_names=["cno", "engines", "number"])
result["engines"] = result["engines"].str.extract("\d*\*\d*\*([\d\.]*)").replace('', '0').fillna(0)
result["engines"] = result["engines"].astype('float64')
engine_number_list = [re.findall(r'(?:.+?\*)(\d+)', _) for _ in result["number"]]
result["number"] = [sum([int(num) for num in num_list]) for num_list in engine_number_list]
result["total_power"] = result["number"] * result["engines"]
# write_to_sql(result, 'CCS_temp', 'replace')
print(tabulate(result.head(20), headers='keys', tablefmt='psql'))
print(result["number"].str.extract("(\d(?=;)|\d(?=[; a-zA-Z0-9]*)\*\d)"))
print(tabulate(result.head(100), headers='keys', tablefmt='psql'))




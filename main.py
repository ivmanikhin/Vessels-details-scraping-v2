import time

import pandas as pd
import sqlite3
import re
import numpy as np
from ABS_parser import ABS
from tabulate import tabulate
import asyncio
import os
import pprint

SEP = os.sep

DATA_TYPES = {
    "int": "Integer",
    "float": "Real",
    "str": "Text",
    "object": "Text"
}

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_rows", None)
pd.set_option('max_colwidth', None)


def new_column_to_sql(con, df, table_name):
    cur = con.cursor()
    try:
        cur.execute(f"PRAGMA table_info({table_name})")
        db_columns = pd.DataFrame(cur.fetchall())[1].to_list()
        for col_name in list(df.columns.values):
            if col_name not in db_columns:
                print(f"New column: \"{col_name}\"")
                data_type_py = re.search("([a-zA-Z]+)", str(df.dtypes[col_name])).group(1)
                print(f"Python data type: \"{data_type_py}\"")
                data_type_sql = DATA_TYPES[data_type_py]
                print(f"SQL data type: \"{data_type_sql}\"")
                cur.execute(f"PRAGMA table_info({table_name})")
                cur.execute(f"ALTER TABLE {table_name} ADD COLUMN `{col_name}` {data_type_sql}")
    except:
        pass


def write_to_sql(df, table_name):
    con = sqlite3.connect(f'data{SEP}ships.db')
    new_column_to_sql(con, df, table_name)
    df.to_sql(name=table_name, con=con, if_exists="append", index=False)
    con.close()


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


cnos_list = read_txt_to_list(f"ABS_parser{SEP}cnos_list.txt")
print(f"Total {len(cnos_list)} vessels")
search_list = make_search_list(cnos_list, 100)
print(f"{len(search_list)} batches with {len(search_list[0])} elements each")
time.sleep(3)
i = 0
for cnos_list in search_list[86:]:
    i += 1
    print(f"Batch {i} of {len(search_list)}")
    time.sleep(2)
    asyncio.run(ABS.parse_cnos_list(cnos_list))
    ships_details_batch = []
    for raw_data in ABS.results:
        try:
            ships_details = ABS.raw_data_to_dict(raw_data)
            ships_details_batch.append(ships_details)
        except:
            pass
    result = pd.DataFrame.from_dict(ships_details_batch)
    print(tabulate(result, headers='keys', tablefmt='psql'))
    write_to_sql(result, "ABS_details")
    ABS.results.clear()



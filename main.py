# import time
import DNV_parser.constants
from CCS_parser import CCS
import pandas as pd
# import multiprocessing as mp
import sqlite3
# import numpy as np
import re
import numpy as np
from tabulate import tabulate

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
                cur.execute(f"ALTER TABLE {table_name} ADD COLUMN `{col_name}`")
    except:
        pass


def write_to_sql(df, table_name):
    con = sqlite3.connect('data/ships.db')
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


cnos_list = read_txt_to_list("CCS_parser/cnos_list.txt")
search_list = make_search_list(cnos_list, 50)
for batch in search_list:
    print(batch)
    ship_details_df = CCS.parse_list(batch)
    print(tabulate(ship_details_df, headers='keys', tablefmt='psql'))
    write_to_sql(ship_details_df, "CCS_details")





# ship_details = CCS.get_ship_details("00D6006")
# print(tabulate(ship_details, headers='keys', tablefmt="psql"))

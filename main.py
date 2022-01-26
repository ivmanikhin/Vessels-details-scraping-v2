from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from IRS_parser import IRS
from ABS_parser import ABS
from tabulate import tabulate
import asyncio
import os
from easy_SQL.easy_SQL import *
import pprint
import time
import seaborn as sns
from scipy import stats

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


# dataset = extract_table_from_sql(table_name="RS_details", sql_column_names="RSNo, MainEngine", df_column_names=["cno", "power"])
# # dataset["power"] = dataset["power"].str.extract("power of ME: ([\d\.\* ]*) Mark ME").replace('', '0').fillna(0)
# # dataset["engines"] = dataset["engines"].astype('float64')
# engine_number_list = [[re.findall(r"(?:power of ME: )([\d\.\* ]*)(?: Mark ME)", _) if _ is not None else ['0']] for _ in dataset["power"]]
# dataset["power"] = ['+'.join(_[0]) for _ in engine_number_list]
# dataset = dataset.fillna("0")
# dataset["power"] = dataset["power"].map(eval)
# # dataset["total_power"] = dataset["number"] * dataset["engines"]
# write_to_sql(dataset, 'RS_temp', 'replace')
# print(dataset)
# # print(tabulate(dataset, headers='keys', tablefmt='psql'))
#
# # dataset["MainEngine"] = database["Number and power of generators"].str.replace("\* ", "*").str.replace(" ", "+").fillna(value=0).astype(str)
# # dataset["Total engine power"] = database["Main Engine"].map(eval)

dataset = extract_table_from_sql(table_name="main_ships_data_raw",
                                 sql_column_names="loa, boa, draft, speed, power",
                                 df_column_names=["loa", "boa", "draft", "speed", "power"],
                                 additional_parameters="where (loa * boa * draft > 1000) and loa > 10 and boa > 2 and draft > 0.5 and draft < 30 and speed < 100 and speed > 0.1 and power < 100000 and power > 1")
# print(tabulate(dataset.head(50), headers='keys', tablefmt='psql'))
dataset = dataset.sample(frac=0.1)
dataset["loa"] = dataset["loa"].astype("float64")
dataset["boa"] = dataset["boa"].astype("float64")
dataset["draft"] = dataset["draft"].astype("float64")
dataset["power"] = dataset["power"].astype("float64")
dataset["speed"] = dataset["speed"].astype("float64")
print(dataset.shape)
dataset["vol"] = dataset["loa"] * dataset["boa"] * dataset["draft"]
dataset["cx"] = dataset["power"] / dataset["speed"]
dataset["fatness"] = dataset["loa"] / dataset["boa"]

good_rows = (np.abs(stats.zscore(dataset)) < 3).all(axis=1)
dataset = dataset[good_rows]
print(dataset.shape)


# X, Y = np.meshgrid(x, y)

plt.rcParams["figure.figsize"] = (8,6)
ax = plt.axes(projection='3d')
ax.scatter(dataset["vol"], dataset["power"], dataset["speed"], s=1, c=dataset["fatness"])
ax.set_xlabel("volume")
ax.set_ylabel("power")
ax.set_zlabel("speed")
# plt.tricontourf(dataset["vol"], dataset["cx"], dataset["fatness"])
plt.show()




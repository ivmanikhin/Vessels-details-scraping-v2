# def get_cno_batch(search_request, q):
#     with BV.BV() as bot:
#         bot.land_search_page()
#         cno_list = bot.get_cno_list(search_request)
#     # df = BV.parse_list(cno_list)
#     # return df
#     q.put(cno_list)


# def parallel_run(request_list):
#     q = mp.Queue()
#     cno_list = []
#     proc_list = [mp.Process(target=get_cno_batch, args=(req, q)) for req in request_list]
#     for proc in proc_list:
#         proc.start()
#         time.sleep(1)
#     for proc in proc_list:
#         cno_list += q.get()
#         proc.join()
#     return cno_list


# letters = DNV_parser.constants.LETTERS
# words = []
# for letter1 in letters:
#     for letter2 in letters:
#         for letter3 in letters:
#             words.append(str(letter1 + letter2 + letter3))
# print(words)

# search_list = make_search_list(DNV.consts.WORD_LIST, batch_size=50)
# final_cnos_list = []
# for words_batch in search_list:
#     cnos_list = DNV.get_cnos_list(words_batch)
#     final_cnos_list += cnos_list
#     final_cnos_list = list(set(final_cnos_list))
#     print(f"Final CNOs list length: {len(final_cnos_list)}\n\n\n")
#     write_list_to_txt(final_cnos_list, filename="DNV_parser\DNV_cnos_list", mode="w")
#
# write_list_to_txt(final_cnos_list, filename="DNV_parser\DNV_final_cnos_list", mode="w")




# for letter1 in LETTERS:
#     for letter2 in LETTERS:
#         word = letter1 + letter2
#         word_list.append(word)
#
# print(word_list)


# _ = 0
# while True:
#     _ += 1
#     print(f"Current page is {_}")
#     cnos_batch = DNV.get_cnos_list(_, 100)
#     print(cnos_batch)
#     if len(cnos_batch) > 0:
#         ships_info_batch = BV.parse_list(cnos_batch)
#         print(ships_info_batch)
#         write_to_sql(ships_info_batch)
#     else:
#         break




# search_list = make_search_list(1, 14, 5)
# print(search_list)
# cno_list = []

# if __name__ == '__main__':
#     mp.set_start_method('spawn')
#     for sublist in search_list:
#         print(sublist)
#         cno_list += parallel_run(sublist)
#         cno_list = list(set(cno_list))
#         print(cno_list)
#         print(len(cno_list))
#         print(f"Finally\n{cno_list}")

# write_to_sql(df)

# bot.parse_page()


# with open(r"NKK_parser\NKK_cno_list.txt", "r") as file:
#     cno_list = file.read().split("\n")
# bot = NKK()
# bot.land_links_page()
# database = bot.get_ship_details(cno_list[0])

# for cno in cno_list:
#     df = bot.get_ship_details(cno)
#     database = pd.concat([database, df], ignore_index=True, axis=0)
#     print(database.tail(1))
#     print(database.shape)
#     if len(database) % 101 == 0:
#         database = database.drop([0], axis=0)
#         con = sqlite3.connect('ships_test.db')
#         new_column_to_sql(con)
#         database.to_sql(name="NKK_details", con=con, if_exists="append", index=False)
#         con.close()
#         database = database.iloc[-1:]
# bot.quit()

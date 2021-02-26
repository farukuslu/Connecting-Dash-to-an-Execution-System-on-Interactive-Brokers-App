# Contains helper functions for your apps!
import os
from os import listdir, remove

# If the io following files are in the current directory, remove them!
# 1. 'currency_pair.txt'
# 2. 'currency_pair_history.csv'
# 3. 'trade_order.p'

# def check_for_and_del_io_files():
#     deleted_file_list = ['currency_pair.txt', 'currency_pair_history.csv', 'trade_order.p']
#     for file_name in deleted_file_list:
#         if os.path.exists(file_name):
#             os.remove(file_name)
#             print(file_name + " deleted successfully from the directory.")
#         else:
#             print(file_name + " doesn't exists in the directory.")
#     pass  # nothing gets returned by this function, so end it with 'pass'.

def check_for_and_del_io_files(file_name):
    deleted_file_list = ['currency_pair.txt', 'currency_pair_history.csv', 'trade_order.p']
    if deleted_file_list and os.path.exists(file_name):
        os.remove(file_name)
        print(file_name + " deleted successfully from the directory.")
    else:
        print(file_name + " doesn't exists in the directory.")
pass  # nothing gets returned by this function, so end it with 'pass'.


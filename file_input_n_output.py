# File input & output!
# Use to talk between the two apps.

# Here's a good site with lots of practice data like the below:
# https://github.com/plotly/datasets

import pandas as pd

# 1) Read a CSV from URL
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

# 2) Save a CSV
df.to_csv('aaxxxpl_data.csv')

# 3) Read a CSV from file
nother_csv = pd.read_csv('aapl_data.csv')

# 4) Make a dictionary
action = 'BUY'
trade_currency = 'EURUSD'
trade_amt = 20000

# trade_order is a dictionary -- you can retrieve its different elements as shown below.
trade_order = {
    "action": action,
    "trade_currency": trade_currency,
    "trade_amt": trade_amt
}

print(trade_order)

# Retrieve elements from the dictionary:
# Retrieve the action
print(trade_order['action'])
# Retrieve the trade_currency
print(trade_order['trade_currency'])
# Retrieve the trade amount
print(trade_order['trade_amt'])

# 5) Save that dictionary.
# We'll need another module...
import pickle

pickle.dump(trade_order, open("trade_order.p", "wb"))

# 6) Read the pickle back...
some_var_w_pickle_data = pickle.load(open("trade_order.p", "rb"))
print(some_var_w_pickle_data)

# 7) Write a text file
some_var_that_I_want_to_write_as_text = "Jake^2"
file_to_write_to = open("file_w_jakes.txt", "w")
file_to_write_to.write(some_var_that_I_want_to_write_as_text)
file_to_write_to.close()

# 8) Read from a text file
file_to_read_from = open('file_w_jakes.txt', 'r')
info_from_file=file_to_read_from.read()
print(info_from_file)
file_to_read_from.close()

# 9) Working with directories
import os

# Print everything in the current directory
print(os.listdir())

print('file_w_jakes.txt' in os.listdir())

# 10) Delete a file
os.remove("file_w_jakes.txt")

print(os.listdir())

print('file_w_jakes.txt' in os.listdir())



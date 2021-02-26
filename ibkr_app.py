from ib_insync import *
from os import listdir, remove
from time import sleep
import pickle
import pandas as pd
from helper_functions import *

# Define your variables here ###########################################################################################
sampling_rate = 10 # How often, in seconds, to check for inputs from Dash?

# For TWS Paper account, default port is 7497
# For IBG Paper account, default port is 4002
port = 7497

# choose your master id. Mine is 10645. You can use whatever you want, just set it in API Settings within TWS or IBG.
master_client_id = 10645

# choose your dedicated id just for orders. I picked 1111.
orders_client_id = 1111
client_id = 3

# account number: you'll need to fill in yourself. The below is one of my paper trader account numbers.
acc_number = 'DU3527359'
########################################################################################################################

# Run your helper function to clear out any io files left over from old runs
#check_for_and_del_io_files('currency_pair_history.csv')

# Create an IB app; i.e., an instance of the IB() class from the ib_insync package
ib = IB()

# Connect your app to a running instance of IBG or TWS
ib.connect(host='127.0.0.1', port=port, clientId=client_id)

# Make sure you're connected -- stay in this while loop until ib.isConnected() is True.
while not ib.isConnected():
    sleep(.01)

# If connected, script proceeds and prints a success message.
print('Connection Successful!')

# Main while loop of the app. Stay in this loop until the app is stopped by the user.
while True:
    # If the app finds a file named 'currency_pair.txt' in the current directory, enter this code block.
    if 'currency_pair.txt' in listdir():

        # Code goes here...
        currency_pair_connection = open('currency_pair.txt', 'r')
        info_from_currency_pair_txt = currency_pair_connection.read()
        currency_pair_connection.close()
        check_for_and_del_io_files('currency_pair.txt')

        #Use the value (which is a string defining a currency pair, e.g., "AUDCAD")
        #to create a contract object of type Forex (from the ib_insync module)
        contract = Forex(info_from_currency_pair_txt)

        # Note that here, if you wanted to make inputs for endDateTime, durationStr, barSizeSetting, etc within the Dash
        #   app, then you could save a dictionary as a pickle and import it here like we do below for the order.
        bars      = ib.reqHistoricalData(
            contract, # <<- pass in your contract object here
            endDateTime='', durationStr='30 D', barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True
        )
        #convert bars to data frame

        #print(bars)
        # currency_pair_data = pd.DataFrame(bars)
        currency_pair_data = util.df(bars)

        # Save a CSV file
        currency_pair_data.to_csv('currency_pair_history.csv')

        # Code goes here...

        # pass -- not return -- because this function doesn't return a value. It's called for what it does. In computer

        #   science, we say that it's called for its 'side effects'.
        pass

    # If there's a file named trade_order.p in listdir(), then enter the loop below.
    if 'trade_order.p' in listdir():

        trd_order = pickle.load(open("trade_order.p", "rb"))
        print(trd_order)

        # Create a special instance of IB() JUST for entering orders.
        # The reason for this is because the way that Interactive Brokers automatically provides valid order IDs to
        #   ib_insync is not trustworthy enough to really rely on. It's best practice to set aside a dedicated client ID
        #   to ONLY be used for submitting orders, and close the connection when the order is successfully submitted.

        # your code goes here
        ib_orders = IB()
        ib_orders.connect(host='127.0.0.1', port=port, clientId=orders_client_id, account=acc_number)

        # "action": action,
        # "trade_currency": trade_currency,
        # "trade_amt": trade_amt

        contract = Forex(trd_order['trade_currency'])
        order = MarketOrder(trd_order['action'], trd_order['trade_amt'],)
        new_order = ib.placeOrder(contract, order)
        ib.sleep(1)
        new_order.log

        # The new_order object returned by the call to ib_orders.placeOrder() that you've written is an object of class
        #   `trade` that is kept continually updated by the `ib_insync` machinery. It's a market order; as such, it will
        #   be filled immediately.
        # In this while loop, we wait for confirmation that new_order filled.
        while not new_order.orderStatus.status == 'Filled':
            ib_orders.sleep(0) # we use ib_orders.sleep(0) from the ib_insync module because the async socket connection
                               # is not built for the normal time.sleep() function.

        # your code goes here
        check_for_and_del_io_files('trade_order.p')
        # pass: same reason as above.
        pass

    # sleep, for the while loop.
    ib.sleep(sampling_rate)

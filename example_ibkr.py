# Example connection to Trader Workstation (TWS) or IB Gateway (IBG)
from ib_insync import *
from time import sleep

# Don't forget to open TWS or IBG and sign into a paper account!
# Also don't forget to allow API connections in Global Configuration > API Settings.

# For TWS Paper account, default port is 7497
# For IBG Paper account, default port is 4002
port = 4002
# choose a client id:
client_id = 3

# Create an IB app; i.e., an instance of the IB() class from the ib_insync package
ib = IB()
# Connect your app to a running instance of IBG or TWS
ib.connect(host='127.0.0.1', port=port, clientId=client_id)

# Make sure you're connected -- stay in this while loop until ib.isConnected() is True.
while not ib.isConnected():
    sleep(.01)

# If connected, script exits the while loop and prints a success message
print('Connection Successful!')

# Request current time
current_time = ib.reqCurrentTime()

# Print current time
print('Current time is: {}'.format(current_time))

# Close IB connection
ib.disconnect()

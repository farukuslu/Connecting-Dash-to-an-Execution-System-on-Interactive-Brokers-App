# HW1: Connecting Dash to an Execution System
This homework will introduce you to the art of communicating between your Python Dash app and a broker's execution system.  We'll be using Trader Workstation (TWS) from Interactive Brokers as the execution system, and a very simple file input & output (i/o) system to achieve communication between Dash and TWS. This *ad hoc* communication design is not intended for production scale applications, but was adopted in this homework for two pedagogical reasons:
1. Students can stop their apps at any time and examine the i/o files using human-readable tools like Excel or Notepad to understand how the data is being passed between the apps.
2. Because they operate in conceptually the same way, this setup prepares the student to understand **sockets**, which *are* suitable for production-level applications.

# Overview
The Flask framework on which Dash is built will **not** allow a connection to Interactive Brokers within a dash app itself, which means that calls to and from TWS can't be made from within Dash. This inconvenience adds a layer of complexity to the system architecture... but not an insurmountable one.
The solution is to run *two apps at the same time*: one (**ibkr_app.py**) that connects to TWS and continually checks for files in the home directory that contain orders from Dash. The other app (**dash_app.py**) provides and receives information from **ibkr_app.py** in the same way -- by looking for and writing files intended for use by **ibkr_app.py**.
### System Architecture
![Overview](www/hw1.png)

# The Rules:
You'll be downloading this repository, finishing the system by writing in yoru own code, and pushing the finished project up to your GitHub repo by the due date. 

It is important that you **do not push or publish any of your code before the assignment is due**. If you finish early, simply email the TA or the Instructor and we'll be happy to grade it for you as soon as we are able.

As long as you keep the repo private, you are welcome to commit & push to your own GitHub account as much as you wish! Doing so is probably a good practice that will keep a backup of your work, and will allow you to easily work from different computers & locations.

# Instructions

## 0. Clone or Download the repo and set up your project.
1. You can either [clone the project in PyCharm](https://www.jetbrains.com/help/pycharm/set-up-a-git-repository.html) or download the repo to your computer as a .zip. Either way, just get the files onto your machine.
2. Once you've cloned to your computer, open the main project folder in PyCharm.
3. You will need to add a virtual environment for this project. Do this by clicking on the "Python" version text at the lower-right hand side of your screen (below), and add a virtual environment (Python 3.9) using "add interpereter". This should add a 'venv' directory to your project.
  
  ![interpreter click](www/click_for_interpreter.png)
  
4. Use pip (Terminal, not Python Console) to install the modules: *dash*, *plotly*, *pandas* and *ib_insync*.

## 1. Confirm your setup
After you open this project in PyCharm, you should be able to do the following to confirm your setup is working:
1. Run the **candlestick_app.py** Dash app
2. Run the **a_button.py** Dash app
3. Run the examples in **file_input_n_output.py**
4. Connect to a paper account -- either your own or the Demo -- using Trader Workstation (TWS) and run **example_ibkr.py**. To be safe, you'll probably want to open up Global Configuration within TWS at File > Global Configuration > API Settings and: 
   * make sure the API socket is allowed
   * the API Read-only box is un-checked
   * confirm the port number that TWS is listening on (it's 7497 by default). 
   You'll know the app works when you can see a success message and the current time (fetched from IBKR's servers) printed in the Python console.
    
If something isn't working, and you can't figure it out, post on the Sakai forum!

## 2. Write yourself a helper function to remove any input/output (i/o) files left over from previous app sessions.
To get started, we'll write a helper function that you'll need in this project. Helper functions are used when you need to perform the same task in a project more than once. 

In this project, we're using two apps (a Dash app and an IBKR app) to communicate with each other by writing and reading files. You'll be running them and stopping them, and sometimes, when you stop them, some of the i/o files may be left undeleted in your folder. Therefore, within each app, you'll need to call a function to make sure that those files are cleared from the home folder.

There are three files in this project that are written and read between the two apps: **'currency_pair.txt'**, **'currency_pair_history.csv'**, and **'trade_order.p'**. 

Use the functions `listdir`() and `remove`(), both from the `os` module, to complete the helper function `check_for_and_del_io_files`() in the 'helper_functions.py' file. There are examples using these functions in the 'file_input_n_output.py' file in this repo. You can complete the `check_for_and_del_io_files`() function by **writing `if` statement(s)** that:
1. Check to see if any of the three files above are present in the home directory
2. If one or more is present, delete them
3. If not, do nothing.

You can create dummy files having one of the names above using Notepad or Excel, then see if your function properly removes them if they're present.

**Note that you can put any number of helper functions in this file if you see the need while you complete this HW!!!**

## 3. Complete your Dash app
The file 'dash_app.py' contains the Dash component of this project, and you'll need to write it in order for it to funciton. When you're finished, your Dash app should be able to display the OHLC history of a currency pair you select, as well as enter Market Order trades to your paper trading account. 

You can write the app by following the comments I've provided in the 'dash_app.py' file to accomplish the following:
1. Run `check_for_and_del_io_files`() to remove any i/o files. Note how it's imported with the command `from helper_functions import *`. Recall that the `*` means "every function in the file".
2. Complete the app's layout. I've provided comments and empty lines in the 'dash_app.py' code for each item. You will the Dash Tutorial (and other info) on the [Dash Website](https://dash.plotly.com/), as well as examples provided in this repo and in class, to be extremely helpful!:
   * A *text input* object that takes in a currency pair. You should provide an initial value for this input; for example, "AUDCAD". I've provided a bit of styling for you in the code.
   * A *Submit Button* that, when clicked, updates the candlestick chart
   * A *div* for text output that displays the currency pair that has just been queried when the Submit button is pressed. It should initially display some instructions like 'Enter a currency code and press 'submit'' as a `children` attribute.
   * A **Graph object** to display the candlestick chart. Use the helper app provided in this repo.
   * An **output div** to confirm what trade was made when you click 'Trade'. You don't have to initialize this div with any children attribute.
   * A **radio input** that allows you to select "BUY" or "SELL" when making a trade. [This Example](https://dash.plotly.com/dash-core-components/radioitems) can help you.
   * A **text input** that contains the name of the currency pair the user wishes to trade (e.g., "EURUSD")
   * A **numeric input** for trade amount (how much currency does user want to trade?)
   * A **submit button** that says "Trade" -- when pressed, will execute the order defined by the buy/sell radio input and the currency pair & the amount defined by the text and numeric inputs.
3. Define a **callback** that runs when the submit button is pressed to retrieve data from IBKR to display in the candlestick plot and update the text output div.
   * You'll need to define two outputs: the output div, for which we want to update the *children* property, and the candlestick graph, for which we want to update the *figure* property.
   * You'll need to pass in the submit button's *n_clicks* property as an input so as to make the callback function run whenever the number of clicks changes (i.e., someone pushes the button)
   * The function needs to know what currency pair you want to query, so it needs the *value* property of the text input that contains the currency pair... but be sure to pass this in as **State**, not an **Input**. If you don't, the app will try to update itself while the user is typing.
4. Write the callback function. `update_candlestick_graph`() should take in `n_clicks` and `value` (from the currency text input) as arguments. The function should then:
   1. Write the value of the currency pair to a file named **currency_pair.txt**
   2. Use a while loop to wait for **ibkr_app.py** (which, when you're using the app, will be running simultaneously) to notice that **currency_pair.txt** has been written, read it in, make the query, and save the resulting data. The while loop should sleep for a small amount of time for as long as **currency_pair_history.csv** -- the data file saved by **ibkr_app.py** -- does not appear in the home directory.
   3. Read in the historical prices from **currency_pair_history.csv**
   4. Remove **currency_pair_history.csv**
   5. Make a candlestick figure from the data in **currency_pair_history.csv**, store as a variable named `fig`
   6. Add an informative title to the candlestick figure
   7. Return the updated div info and the fig to their respective outputs. I've written this line for you so that you can see how it works -- Dash feeds the multiple returns to their outputs in matching order; i.e., the first object listed in the return gets assigned to the first Output in the funciton definition.
5. Define a **callback** that runs when the Trade button is pressed.
   * Needs to know the buy-or-sell value, the name of the pair you want to trade, and the trade amount from the inputs you defined in Section 2 of the layout.
   * There's only one output: the 'children' property of the "trade output" text div you created.
   * Using what you learned above in the first callback, think hard about what variable(s) should cause the function to run when updated. Some should be passed in as State, others as Input.
   * Keep the `prevent_initial_call` parameter set to `True` as I've got it; otherwise, the app will execute a trade as soon as you start it!
6. Write the callback function `trade`().
   1. create a simple output message describing the trade -- can be as simple as you Action, your Trade AMOUNT, and your Trade Pair separated by spaces; e.g., "BUY 20000 EURUSD'. Store this message as the variable `msg`.
   2. create a dictionary named `trade_order` whose elements are named "action", "trade_amt", and "trade_currency", and whose values are the corresponding trade parameters.
   3. Save `trade_order` as a pickle file.
   4. Return `msg` (so that it's written to the div output).
## 4. Complete your IBKR app
Now you need to write the IBKR App: **ibkr_app.py**. This is the app that runs continuously and communicates with TWS. Your code should be written as follows:

1. Define your variables
    * Your IBKR app needs to know a few things to begin with, such as client IDs, port, which account you want to trade with, etc. Provide this info in the boxed-off section.
   
2. Run `check_for_and_del_io_files`()
   
3. Assign the name `ib` to a new instance of the `IB`() app class from `ib_insync`.

4. Connect `ib` to TWS using the port and master client ID you set in your variables. Use localhost (127.0.0.1) for your host.
5. Use a while loop to wait until `ib` is connected to TWS. Print a success message when connected. See **ibkr_app.py** for an example.
   
In the while loop in the main part of the code, write two `if` statements.
6. First `if` statement:
   * check if the file **currency_pair.txt** (which is written by **dash_app.py** when someone presses the Submit button to update the graph) exists in the home directory.
   * If it exists, then:
     1. Open the file and store its value as a variable
     2. Delete the file
     3. Use the value (which is a string defining a currency pair, e.g., "AUDCAD") to create a `contract` object of type `Forex` (from the `ib_insync` module)
     4. Make the request for historical data using the contract object you created. Use the default values I've provided for `endDateTime`, `barSizeSetting`, and so on, but realize (as I've written in the comments) that you could control these parameters within Dash as well if you wanted to. Store the retrieved data as `bars`.
     5. Convert `bars` to a data frame.
     6. Save the data frame as a CSV file named 'currency_pair_history.csv' for the Dash app to find.
     
7. Second `if` statement:
   * check if the file **trade_order.p** (which is written by **dash_app.py** when someone presses the Trade button to make a trade) exists in the home directory.
   * If it exists, then:
      1. Load the **trade_order.p** pickle into a variable named `trd_ordr` (which is a dictionary).
      2. Use `trd_ordr` to create a `contract` object of type `Forex` and an `order` object of type `MarketOrder`. You can easily do this by passing in the proper values from `trd_ordr` to the functions `MarketOrder` and `Forex`, which are provided by `ib_insync`.
     3. Set the `account` property of the `order` object to `acc_number`, which you provided at the beginning of your script (it's the paper account that you want to use for your trades.)
     4. Create **another** instance of class `IB`(). This time, name it "`ib_orders`" because it will be used for submitting orders only.
     5. Connect `ib_orders` to TWS using `orders_client_id`, the client ID you defined at the beginning of the file and set aside for trade orders.
     6. Place the order! use the `ib_orders.placeOrder()` method, and store the result in a variable named `new_order`.    7. Take a look at the while loop and the commentary I've written, which waits for the market order you submitted to fill before proceeding. You don't need to write any code here -- just understand it.
     8. After the order fills, delete 'trade_order.p'
     9. disconnect `ib_orders`
   
# 5. Run it!
1. Open up TWS and log in to a paper account.
2. Enter in the parameters you need in the **ibkr_app.py** file -- account number, id, etc -- if you haven't already.
3. Run **dash_app.py** and **ibkr_app.py** in PyCharm (order doesn't matter)
4. Visit [IBKR's Forex Product Listing](https://www.interactivebrokers.com/en/index.php?f=2222&exch=ibfxpro&showcategories=FX) to view all of the possible currency pairs.
   
If all went well, you should be able to open your Dash app in the browser and query price history for the currency pairs listed at the site above, as well as make trades! Watch your open TWS window to make sure your trades go through.

CONGRATULATIONS! You've made your first fully-funcitonal, round-trip trading app.
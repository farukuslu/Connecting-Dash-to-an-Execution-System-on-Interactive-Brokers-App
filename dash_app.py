import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
from os import listdir, remove
import pickle
import os
import time

from helper_functions import * # this statement imports all functions from your helper_functions file!

# Run your helper function to clear out any io files left over from old runs
# 1:
#check_for_and_del_io_files()
#check_for_and_del_io_files('currency_pair_history.csv')
check_for_and_del_io_files('currency_pair.txt')
check_for_and_del_io_files('trade_order.p')

# Make a Dash app!
app = dash.Dash(__name__)

# Define the layout.
app.layout = html.Div([
    # Section title
    html.H1("Section 1: Fetch & Display exchange rate historical data"),

    # Currency pair text input, within its own div.
    html.Div(
        [
            "Enter a currency code and press 'submit': ",
            # Your text input object goes here:
            dcc.Input(id = 'input_currency_pair', value='EURUSD', type = 'text')
        ],
        # Style it so that the submit button appears beside the input.
        style={'display': 'inline-block'}
    ),
    # Submit button:
    html.Button('Submit', id='submit_currency_pair', n_clicks=0),

    # Div to hold the initial instructions and the updated info once submit is pressed
    html.Div(id='output_currency_pair'),

    # Line break
    html.Br(),
    # Candlestick graph goes here:
    dcc.Graph(id="graph"),

    # Another line break
    html.Br(),

    # Section title
    html.H1("Section 2: Make a Trade"),

    # Div to confirm what trade was made

    html.Div(id='trade_output'),

    # Radio items to select buy or sell
    html.Div([
        dcc.RadioItems(
            id='input_action',
            options=[
                {'label': 'BUY', 'value': 'BUY'},
                {'label': 'SELL', 'value': 'SELL'}],
            value='BUY',
            labelStyle={'display': 'inline-block'}
        )
    ]),

    # Another line break
    html.Br(),

    # Text input for the currency pair to be traded
    html.Div(
        [
            "Currency   Pair:  ",
            # Your text input object goes here:
            dcc.Input(id='input_trade_currency', value='EURUSD', type='text')
        ],
        # Style it so that the submit button appears beside the input.
        style={'display': 'inline-block'}
    ),

    # Another line break
    html.Br(),

    # Numeric input for the trade amount
    html.Div(
        [
            "Trade Amount: ",
            # Your text input object goes here:
            dcc.Input(id = 'input_trade_amt', value='00', type = 'number')
        ],
        # Style it so that the submit button appears beside the input.
        style={'display': 'inline-block'}
    ),

    # Submit button for the trade
    html.Button(['Trade'], id='submit_trade', n_clicks=0),
])

# Callback for what to do when submit-button is pressed/
@app.callback(
    [dash.dependencies.Output('output_currency_pair', 'children'),
     dash.dependencies.Output('graph', 'figure')],
    [dash.dependencies.Input('submit_currency_pair', 'n_clicks')],
    [dash.dependencies.State('input_currency_pair', 'value')]
)
def update_candlestick_graph(n_clicks, value): # n_clicks doesn't get used, we only include it for the dependency.

    # Now we're going to save the value of currency-input as a text file.
    currency_to_write_to_txt = '{}'.format(value)
    file_to_write_to = open("currency_pair.txt", "w")
    file_to_write_to.write(currency_to_write_to_txt)
    file_to_write_to.close()

    #Wait until ibkr_app runs the query and saves the historical prices csv
    file_path = 'currency_pair_history.csv'

    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.exists(file_path):
        # Read in the historical prices
        df = pd.read_csv(file_path)
        # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
    else:
        raise ValueError("%s isn't a file!" % file_path)

    # Remove the file 'currency_pair_history.csv'
    #check_for_and_del_io_files('currency_pair_history.csv')

    print(type(df))
    # print(df)

    #Make the candlestick figure
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close']
            )
        ]
    )

    # fig = go.Figure(
    #     data=[
    #         go.Candlestick(
    #             x=df['Date'],
    #             open=df['AAPL.Open'],
    #             high=df['AAPL.High'],
    #             low=df['AAPL.Low'],
    #             close=df['AAPL.Close']
    #         )
    #     ]
    # )

    # Give the candlestick figure a title
    fig.update_layout(title='Candlestick Graph', xaxis_rangeslider_visible='slider' in value),
    check_for_and_del_io_files('currency_pair_history.csv')

    #Return your updated text to currency-output, and the figure to candlestick-graph outputs
    return ('Submitted query for ' + value), fig

#Callback for what to do when trade-button is pressed
@app.callback(
    dash.dependencies.Output('trade_output', 'children'),
    dash.dependencies.Input('submit_trade', 'n_clicks'),
    [dash.dependencies.State('input_action', 'value'),
    dash.dependencies.State('input_trade_currency', 'value'),
    dash.dependencies.State('input_trade_amt', 'value')],
    # We DON'T want to start executing trades just because n_clicks was initialized to 0!!!
    prevent_initial_call=True
)
def trade(n_clicks, action, trade_currency, trade_amt): # Still don't use n_clicks, but we need the dependency

    # Make the message that we want to send back to trade-output
    msg = 'Right now, your trade order: {}, {}, {}'.format(action,trade_currency,trade_amt)
    print(msg)
    print(type(action))
    print(type(trade_currency))
    print(type(trade_amt))

    # Make our trade_order object -- a DICTIONARY.
    trade_order = {
        "action": action,
        "trade_currency": trade_currency,
        "trade_amt": trade_amt
    }

    # Dump trade_order as a pickle object to a file connection opened with write-in-binary ("wb") permission:
    pickle.dump(trade_order, open("trade_order.p", "wb"))

    # Return the message, which goes to the trade-output div's "children" attribute.
    return msg

# Run it!
if __name__ == '__main__':
    app.run_server(debug=True)

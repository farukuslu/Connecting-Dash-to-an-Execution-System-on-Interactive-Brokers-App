# How to make and use a button

# make your imports
import dash
import dash_html_components as html
import dash_core_components as dcc

# create an app object of class 'Dash'
app = dash.Dash(__name__)

# Define the layout of the dash page.
app.layout = html.Div([
    html.Div(dcc.Input(id = 'currency-pair', type = 'text')),
    html.Button('Submit', id = 'submit-button', n_clicks = 0),
    html.Div(id='output-div', children='This is a default value.')
])

@app.callback(
    dash.dependencies.Output('output-div', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('currency-pair', 'value')]
)

def write_something_to_the_div(n_clicks, value):
    message_to_write_to_div = 'Right now, the value in the input is {}, and the submit button has been clicked {} times.'.format(
        value,
        n_clicks
    )
    return message_to_write_to_div


if __name__ == '__main__':
    app.run_server(debug=True)

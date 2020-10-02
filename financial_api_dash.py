import pandas as pd
import plotly
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# 'pip install alpha_vantage'
from alpha_vantage.timeseries import TimeSeries

#----------------------------------------------------------------------------------------------------
# Set up inital key and financial category

# API Key
key = 'JJ9K7NYA6WN0QYY8'

# Choose output for format for python dict (or else default to JSON)
# Options are 'pandas', 'json', or 'csv'
ts = TimeSeries(key, output_format='pandas')

#----------------------------------------------------------------------------------------------------
# Test for processing data
# amd_data, amd_meta_data = ts.get_intraday(symbol='AMD', interval='1min', outputsize='compact')
# print(amd_meta_data)

# df = amd_data.copy()
# print(df.head())

# df = df.transpose()
# print(df.head())

# df.rename(index={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'}, inplace=True)
# df = df.reset_index().rename(columns={'index': 'indicator'})
# print(df.head())

# df = pd.melt(df, id_vars=['indicator'], var_name = 'date', value_name='rate')
# df = df[df['indicator']!= 'volume']
# print(df[:15])

#----------------------------------------------------------------------------------------------------
# Build web app + automatically update financial data

# Init app
app = dash.Dash(__name__)

# Create page layout
app.layout = html.Div([
    # Interval is invisible on page and tells app how long to update
    dcc.Interval(
                id='my_interval',
                n_intervals=0,            # number of times interval is activated
                interval=120*1000       # update every 2 min (120 sec * 1000 milisec)
    ),
    dcc.Graph(id='world_finance')      # empty graph that will be populated with line chart
])

#----------------------------------------------------------------------------------------------------
# Attach chart to backend

# App callback
@app.callback(
    Output(component_id='world_finance', component_property='figure'),
    [Input(component_id='my_interval', component_property='n_intervals')]
)
def update_graph(n):
    """Pull financial data from Alpha Vantage and update grapp every 2 min

    Args:
        n ([df]): returns line chart
    """

    amd_data, amd_meta_data = ts.get_intraday(symbol='AMD', interval='1min', outputsize='compact')
    df = amd_data.copy()
    df = df.transpose()
    df.rename(index={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'}, inplace=True)
    df = df.reset_index().rename(columns={'index': 'indicator'})
    df = pd.melt(df, id_vars=['indicator'], var_name = 'date', value_name='price')
    df = df[df['indicator']!= 'volume']
    print(df[:15])

    line_chart = px.line(
                    data_frame=df,
                    x='date',
                    y='price',
                    color='indicator',
                    title='Stock: {}'.format(amd_meta_data['2. Symbol'])
    )
    return (line_chart)

#----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
    


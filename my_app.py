# Import libraries
from dash import Dash, dcc, html, page_registry, page_container
import dash_bootstrap_components as dbc
import os
#import dash_bootstrap_components as dbc
#import numpy as np
#import pandas as pd
#import xarray as xr

#import sys
#print(sys.executable)
print('hello')

thisPath = os.path.abspath(os.path.dirname(__file__))
#print(dash.__version__)
#print(np.__version__)
#print(pd.__version__)
#print(xr.__version__)
#print(dbc.__version__)

app = Dash(__name__, use_pages=True)

server = app.server

app.layout = html.Div([
            # Framework of the main app
            html.Div("The Science and Ethics of Fair Shares dashboard", style={'fontSize':50, 'textAlign':'center'}),
            html.Div([
                dcc.Link(page['name']+"  |  ", href=page['path'])
                for page in page_registry.values()
            ]),
            html.Hr(),
            #Content of each page
            page_container
            #dcc.Location(id='url', refresh=False),
            #html.Div(id='page-content'),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
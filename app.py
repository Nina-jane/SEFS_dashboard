# Import libraries
import dash
from dash import Dash, dcc, html

#from dash.dependencies import Input, Output

#import pandas as pd
#import plotly.express as px

#import plotly.graph_objects as go #Used a few times in commented out code for graphs
#import numpy as np #Used a few times in commented out code for graphs

#import glob #Used once
import os #Used 11 times to join paths
#import dash_bootstrap_components as dbc #Used a lot for the layout of functions

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
## app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
##external_stylesheets = ['https://www.herokucdn.com/purple3/latest/purple3.min.css']


#### COMMENTED OUT AND TESTING ####
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# app = dash.Dash(__name__)
# server = app.server
# app.scripts.config.serve_locally = True
# app.config['suppress_callback_exceptions'] = True

thisPath = os.path.abspath(os.path.dirname(__file__))
#print(dash.__version__)
app = Dash(__name__)
#use_pages=True)

server = app.server

app.layout = html.Div([
            # Framework of the main app
            html.Div("The Science and Ethics of Fair Shares dashboard", style={'fontSize':50, 'textAlign':'center'}),
            html.Div([
                dcc.Link(page['name']+"  |  ", href=page['path'])
                for page in dash.page_registry.values()
            ]),
            html.Hr(),
            #Content of each page
            dash.page_container
            #dcc.Location(id='url', refresh=False),
            #html.Div(id='page-content'),
    ]
)

# @app.callback(dash.dependencies.Output('page-content', 'children'),
#               [dash.dependencies.Input('url', 'pathname')])
# def display_page(pathname):
#     #if pathname == '/Able':
#     #    return APP_page
#     if pathname == '/Contributions':
#         return contributions_page
#     elif pathname == '/Dist_costs':
#         return costs_page
#     elif pathname == '/Dist_rights':
#         return rights_page
#     elif pathname == '/Meth':
#         return methodology_page
#     elif pathname == '/Refs':
#         return ref_page    
#     else:
#         return about_page
        
# external_stylesheets = [
#     'https://codepen.io/chriddyp/pen/bWLwgP.css',
#     {
#         'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
#         'rel': 'stylesheet',
#         'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
#         'crossorigin': 'anonymous'
#     }


if __name__ == "__main__":
    app.run(debug=True)
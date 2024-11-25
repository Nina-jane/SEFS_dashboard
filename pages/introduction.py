import dash
from dash import html,dcc

dash.register_page(__name__, path='/')

layout = html.Div([

    html.Div(
        children=[
            html.Div(
                className="user-selections-party-p1",
                children=[
                    html.Div([
                        #html.H1('The Warming & Distributive Justice dashboard', className="app-header--title", style={'textAlign': 'left'}),
                        #html.Img(src='/assets/W&R_2.png', className="dashboard-image"),
                        html.H1("Background"),
                        html.P([
                            '''This dashboard supports consideration of three climate change-related questions, listed below.''', html.Br(),html.Br(),'''
                                    
                            - What are countries\' contributions to global warming?''', html.Br(),'''
                            - How should the costs of climate change be distributed amongst countries?''', html.Br(),'''
                            - How should future emissions rights or 'warming' rights be distributed amongst countries?''', html.Br(), html.Br(),'''

                            The first question is related to climate science, while questions two and three fall under distributive justice (an area of applied climate ethics).''', html.Br(),html.Br(),'''
                                        
                            To help answer these questions, the dashboard combines data from a range of sources. Several of these have been listed below.''', html.Br(),html.Br(),'''
                                        
                            - The World Development Bank''', html.Br(),'''
                            - UNFCCC GHG national inventories'''], style={'textAlign': 'left'}
                            ),
                        html.Button("Update"),
                        ], id='left-container')
                ]
            )
        ]
    )
])

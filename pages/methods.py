import dash
from dash import html, dash_table
import pandas as pd
#import os

dash.register_page(__name__)

#thisPath = os.path.abspath(os.path.dirname(__file__))

image_path = 'assets/rights_diagram.png'

df = pd.read_csv('methods_table.csv', encoding='cp1252')

layout = html.Div([

    html.Div([
        #className="app-header",
        #children = [
        #    html.Div('Methodology', className="app-header--title")
        #]
        html.H1('Methods', style={'textAlign': 'left'}),
        html.P(['''Creating the SEFS dashboard involved drawing upon knowledge and methods from four main disciplines, including:''']),
        html.Li(['''Climate science''']),
        html.Li(['''Industrial ecology''']),
        html.Li(['''Applied ethics''']),
        html.Li(['''Data science''']),

        html.P(['''The specific methods from each of these disciplines are named and described in the table below.''']),

        dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns],
                             style_header={
                                 'fontWeight': 'bold'
                             },
                             style_cell={
                                 'whiteSpace': 'normal',
                                 'height': 'auto',
                                 #'maxWidth': '700px',
                                 'font_family': 'Arial',
                                 'font_size': '16px',
                                 'text-align': 'left'
                             },
                             style_data_conditional=[{
                                 "if": {"column_id": 'Discipline'},
                                 "fontWeight": "bold",
                             }],
        ),

        html.H2('Calculations')

        # html.H2(['Methodological approach']),
        # html.P(['''This research spans the domains of climate science, climate economics and climate ethics. A wide range of methods have been used to gain insights from the data. These are listed below.
        #         -	Input-output analysis
        #         -   General data science techniques''']),
        # html.H2(['Contributions to global warming page']),
        # html.P(['''Countries contribute to global warming by emitting greenhouse gases (GHGs). The Contributions to warming page of the dashboard displays xxx countries’ GHG emissions data for the three main GHGs – carbon dioxide (CO\N{SUBSCRIPT TWO}), methane (CH\N{SUBSCRIPT FOUR}) and nitrous oxide (N\N{SUBSCRIPT TWO}O) – between 1990-2015. Also displayed are how a country’s CO2, CH4 and N2O emissions have contributed towards global warming.
        #         The panel to the left enables users to select from a range of different options and observe how a different country’s contributions to global warming (from these three main GHGs) changes, as different choices are made.
        #         For instance, users can select a different country and a year range between 1990-2015. These choices will update the three line graphs at the top of the page and the pie charts at the bottom of the page.
        #         The second two choices will update the information in the second row of the dashboard, which has a focus on how much a country has contributed to global warming. All four filters will update this information.
        #         ''']),
        # # See if you can insert the "rights diagram" picture here
        # html.Img(src=image_path, style={'height':'130%', 'width':'130%'})
    ], style={'textAlign': 'left'})], id='methods-container'
)
import dash
from dash import html, dash_table, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import dash_mantine_components as dmc

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
        html.P(['''Creating the SEFS dashboard involved drawing upon knowledge and methods from the following four disciplines:''']),
        html.Div([
            html.Li(['''Simple climate models''']),
            html.Li(['''Industrial ecology''']),
            html.Li(['''Applied ethics''']),
            html.Li(['''Data science''']),
        ], style={'margin-left': '100px'}),

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
                             }])

    ], style={'textAlign': 'left'}, id='left-container-methods'),

    html.Div([

        html.H2('Calculations...'),

        html.H3('For answering RQ1'),

        html.P(['''To calculate countries' contributions to historical global warming, code from the Callahan & Mankin (2022) study was modified to get 
                countries' warming contributions from individual greenhouse gases. This was done by running the code with and without countries' individual
                GHG emissions. Then, the overall differences in global warming btween when countries' GHG emissions were included and excluded was calculated.
                The steps involved with this are detailed below.''']),   

        html.Div(
            [
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        html.P("This is the content of the first section"),
                        title="Polluter Pays",item_id="item-1",className="panel"
                    ),
                    dbc.AccordionItem(
                        html.P("This is the content of the second section"),
                        title="Item 2",item_id="item-2",className="panel"
                    ),
                    dbc.AccordionItem(
                        html.P("This is the content of the third section"),
                        title="Item 3",item_id="item-3",className="panel"
                    ),
                ],
                id="accordion",
                active_item="item-1",
                # start_collapsed=True,
            ),
            html.Div(id="accordion-contents", className="mt-3"),
        ]),
            
        dcc.Markdown('$W_{\\text{warming}_T} = \sum_{y=1850}^{2014} \sum_{i=1}^{174} C_{\\text{warming}_{iy}}, \quad T = \\text{choice of the range of } y$', mathjax=True, style={'textAlign': 'center'}),

        dcc.Markdown('$C\\text{Share}_{iT} = \\frac{C_{\\text{warming}_{iT}}}{W_{\\text{warming}_T}} \cdot F_{\\text{Goal}}, \quad F_{\\text{Goal}} \in \{100,\ 50,\ 25,\ 20,\ 15\}$', mathjax=True, style={'textAlign': 'center'}),      

        #dcc.Markdown('Add text $x=\\frac{-b\\pm\\sqrt{b^2-41c}}{2a}$', mathjax=True, style={'textAlign': 'center'}),

        html.H3('For answering RQ2'),

        html.P(['''To calculate countries' shares of a collective climate mitigation finance goal, several ethical principles were applied. The equations below
                show the calculations that were performed to apply each of the principles.''']),

        html.H3('For answering RQ3'),

        html.P(['''To calculate countries' shares of remaining emissions and warming rights, two principles were applied using the following equations:''']),  

    ], style={'textAlign': 'left'},  id='mid-container-methods')

])


callback(
    Output("accordion-contents", "children"),
    [Input("accordion", "active_item")],
)
def change_item(item):
    return f"Item selected: {item}"
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
        ], style={'margin-left': '60px'}),

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

        html.H1('Calculations...', style={'textAlign': 'left'}),

        # html.H3('For answering RQ1'),

        # html.P(['''To calculate countries' contributions to historical global warming, code from the Callahan & Mankin (2022) study was modified to get 
        #         countries' warming contributions from individual greenhouse gases. This was done by running the python scripts with and without countries' individual
        #         GHG emissions. Then, the overall differences in global warming between when countries' GHG emissions were included and excluded was calculated.
        #         The steps involved with this are detailed below.''']),   


        html.Div(
            children=[
                dmc.Accordion(
                    id="accordion-simple",
                    value=0,
                    children=[
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl("For answering RQ1"),
                                dmc.AccordionPanel(
                                    "To calculate countries' contributions to historical global warming, code from the Callahan & Mankin (2022) study " \
                                    "was modified to get countries' warming contributions from individual greenhouse gases. This was done by running the " \
                                    "python scripts with and without countries' individual GHG emissions. Then, the overall differences in global warming " \
                                    "between when countries' GHG emissions were included and excluded was calculated. The steps involved with this are detailed below. "
                                ),
                            ],
                            value="RQ1",
                        ),
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl("For answering RQ2"),
                                dmc.AccordionPanel(
                                    children=[
                                    "To calculate countries' shares of a collective climate mitigation finance goal, several ethical principles were applied. Equations 1...6 below " \
                                    "show the calculations that were performed to apply each of the principles. ",
                                    html.H4('Polluter Pays equations'),
                                    dcc.Markdown('$W_{\\text{warming}_T} = \sum_{y=1850}^{2014} \sum_{i=1}^{174} C_{\\text{warming}_{iy}}, \quad T = \\text{choice of the range of } y \\tag{3}$', mathjax=True, style={'textAlign': 'left'}),
                                    dcc.Markdown('$C\\text{Share}_{iT} = \\frac{C_{\\text{warming}_{iT}}}{W_{\\text{warming}_T}} \cdot F_{\\text{Goal}}, \quad F_{\\text{Goal}} \in \{100,\ 50,\ 25,\ 20,\ 15\} \\tag{4}$', mathjax=True, style={'textAlign': 'left'}),
                                    html.H4('Beneficiary Pays equations'),
                                    dcc.Markdown('$W_{\\text{wealth}_y} = \sum_{i=1}^{217} C_{\\text{wealth}_{iy}}, \quad y \in [1995, 2018]$', mathjax=True, style={'textAlign': 'left'}),
                                    dcc.Markdown('$CShare_{iy} = \\frac{C_{\\text{wealth}_{iy}}}{W_{\\text{wealth}_y}} \\times FGoal, \quad FGoal \in \{100, 50, 25, 20, 15\} \\tag{5}$', mathjax=True, style={'textAlign': 'left'}),
                                    html.H4('Ability to Pay equations'),
                                    dcc.Markdown('$W_{\\text{GDP}} = \sum_{i=1}^{219} C_{\\text{GDP}_i}$', mathjax=True, style={'textAlign': 'left'}),
                                    dcc.Markdown('$CShare_i = \\frac{C_{\\text{GDP}_i}}{W_{\\text{GDP}}} \\times FGoal, \quad FGoal \in \{100, 50, 25, 20, 15\} \\tag{6}$', mathjax=True, style={'textAlign': 'left'}),                                    
                                    ],
                                ),
                            ],
                            value="RQ2",
                        ),
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl("For answering RQ3"),
                                dmc.AccordionPanel(
                                    children=[
                                    "To calculate countries' shares of a collective global emissions budget, several ethical principles were applied. Equations 7...15 below " \
                                    "show the calculations that were performed to apply each of the principles. "
                                    "Grandfathering equations ",
                                    html.H4('Grandfathering equations'),
                                    dcc.Markdown('$E_T = \sum_{y=1990}^{2015} \sum_{i=1}^{189} C_{iy}, \quad T = \\text{choice of the range of } y$', mathjax=True, style={'textAlign': 'left'}),
                                    dcc.Markdown('$CShare_{iT} = \\frac{C_{iT}}{E_T}, \quad T = \\text{choice of the range of } y$', mathjax=True, style={'textAlign': 'left'}),
                                    dcc.Markdown('$CShare_{iF} = CShare_{iT} \\times BGoal$', mathjax=True, style={'textAlign': 'left'}),
                                    html.H4('Equality-over-time equations'),
                                    dcc.Markdown('$Personyears_{world} = Personyears_{historical} + Personyears_{future}$', mathjax=True, style={'textAlign': 'left'}),
                                    dcc.Markdown('$p_{wTS} = \sum_{y=1850}^{2015} \sum_{i=1}^{174} P_{iy} + \sum_{y=2015}^{2050} \sum_{i=1}^{174} P_{iyS}, \quad S = \{SSP1, SSP2, SSP3, SSP4, SSP5\}$', mathjax=True, style={'textAlign': 'left'}),
                                    dcc.Markdown('$W_T = \sum_{y=1850}^{2014} \sum_{i=1}^{174} C_{iy}, \quad T = \\text{choice of the range of } y$', mathjax=True, style={'textAlign': 'left'}),
                                    dcc.Markdown('$I_{\\text{avg}} = \\frac{1.5 \cdot W_T}{p_{wTS}}$', mathjax=True, style={'textAlign': 'left'}),
                                    dcc.Markdown('$p_{iT} = \\left( \sum_{y=1850}^{2014} P_{iy} + \sum_{y=2015}^{2050} P_{iyS} \\right)$', mathjax=True, style={'textAlign': 'left'}),
                                    dcc.Markdown('$CShare_{iF} = I_{\\text{avg}} \cdot p_{iT} - \sum_{y=1850}^{2014} C_{iy}$', mathjax=True, style={'textAlign': 'left'}),
                                    ],
                                ),
                            ],
                            value="RQ3",
                        ),
                    ],
                ),
                dmc.Text(id="accordion-state", mt=10),
            ]
        ),

        ### Commented out old accordion code below this point

        # html.Div(
        #     [
        #     dbc.Accordion([
        #             dbc.AccordionItem(
        #                 html.P("This is the content of the first section"),
        #                 title="Polluter Pays",item_id="item-1",className="panel"
        #             ),
        #             dbc.AccordionItem(
        #                 html.P("This is the content of the second section"),
        #                 title="Item 2",item_id="item-2",className="panel"
        #             ),
        #             dbc.AccordionItem(
        #                 html.P("This is the content of the third section"),
        #                 title="Item 3",item_id="item-3",className="panel"
        #             ),
        #         ],
        #         id="accordion",
        #         active_item="item-1",
        #         # multiple=True,
        #         # start_collapsed=True,
        #     ),
        #     html.Div(id="accordion-contents", className="mt-3"),
        # ]),

        ### Commented out old accordion code above this point

        # html.H3('For answering RQ2'),

        # html.P(['''To calculate countries' shares of a collective climate mitigation finance goal, several ethical principles were applied. Equations 1...6 below
        #         show the calculations that were performed to apply each of the principles.''']),

        # html.H4('Polluter Pays equations'),
            
        # dcc.Markdown('$W_{\\text{warming}_T} = \sum_{y=1850}^{2014} \sum_{i=1}^{174} C_{\\text{warming}_{iy}}, \quad T = \\text{choice of the range of } y \\tag{3}$', mathjax=True, style={'textAlign': 'left'}),

        # dcc.Markdown('$C\\text{Share}_{iT} = \\frac{C_{\\text{warming}_{iT}}}{W_{\\text{warming}_T}} \cdot F_{\\text{Goal}}, \quad F_{\\text{Goal}} \in \{100,\ 50,\ 25,\ 20,\ 15\} \\tag{4}$', mathjax=True, style={'textAlign': 'left'}),      

        #dcc.Markdown('Add text $x=\\frac{-b\\pm\\sqrt{b^2-41c}}{2a}$', mathjax=True, style={'textAlign': 'center'}),

        
        # html.H3('For answering RQ3'),

        # html.P(['''To calculate countries' shares of remaining emissions and warming rights, two principles were applied using the following equations:''']),

        
    ], style={'textAlign': 'left'},  id='mid-container-methods')

])

### Commented out accordion callbacks below this point

# callback(
#     Output("accordion-contents", "children"),
#     [Input("accordion", "active_item")],
# )
# def change_item(item):
#     return f"Item selected: {item}"


@callback(Output("accordion-state", "children"), Input("accordion-simple", "value"))
def show_state(value):
    return value
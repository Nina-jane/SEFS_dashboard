import dash
from dash import dcc, html, dash_table, callback, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import os
from decimal import Decimal
#import dash_bootstrap_components as dbc

#import xlsxwriter
#import openpyxl

dash.register_page(__name__)

thisPath = os.path.abspath(os.path.dirname(__file__))

# Data required
df_APP_BPP = pd.read_csv(os.path.join(thisPath, os.pardir,'costs_principles_APP_BPP.csv'), index_col=None, encoding='cp1252', low_memory=False)
df_PPP = pd.read_csv(os.path.join(thisPath, os.pardir,'costs_principles_PPP_for_SEFS_online.csv'), index_col=None, encoding='cp1252', low_memory=False)

#df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')

# Set up a dictionary with different finance values
costDictionary = {
    "US$100 billion": 100000000000,
    "US$50 billion": 50000000000,
    "US$20 billion": 20000000000,
    "US$15 billion": 15000000000
}
options=[{'label': i, 'value': i} for i in costDictionary.items()]

principles = ['Ability to Pay', 'Beneficiary Pays', 'Polluter Pays']

radio_country_options = ['All countries', 'Some other number of countries']
radio_sector_options = ['All sectors', 'Single sector']

number_of_countries = {
    "Top 10": 10,
    "Top 20": 20,
    "Top 50": 50,
    "Top 100": 100
}

columns_reordered_APP_BPP = df_APP_BPP[["Rank","Country", "Code", "Value"]]
columns_reordered_PPP = df_PPP[["Rank","Country", "Code", "Finance_share"]]

dates = [1850, 1990, 1960, 2014]

#print(columns_reordered)

layout = html.Div([
    html.Div(
        children=[
            html.Div(
                className="user-selections-party-p1",
                children=[
                    html.Div([
                        html.H1('RQ2: How should the costs of climate change be distributed?'),
                        #html.P(['''This page shows how the costs of climate change (whether they be mitigation, adaptation or loss and damage) ought to be divided amongst countries,
                        #according to the following three principles''']),
                        html.Label('Climate finance amount to be divided between countries / nation states'),
                        html.Br(),
                        html.Br(),
                        dcc.Dropdown(
                            id='finance-amount',
                            options=[{'label': i, 'value': i} for i in costDictionary.keys()],
                            value=list(costDictionary)[0]),
                        
                        html.Label('Principle'),
                        dcc.Dropdown(
                            id='principle-dropdown',
                            options = [{'label': i, 'value': i} for i in principles],
                            value = principles[2],
                            #options = (((df.Principle).dropna()).sort_values(ascending=True)).unique().astype(str), #df.iloc[:,2].unique(),
                            #value = (((df.Principle).dropna()).sort_values(ascending=True)).unique().astype(str), #df.iloc[:,2].unique(),
                            searchable=False),

                        # This one will update the metric dropdown for the APP and BPP
                        html.Div(id='app-bpp-choices-container', children=[
                            html.Label('Dataset'),
                            dcc.Dropdown(
                                id='dataset-dropdown-app-bpp',
                                options = df_APP_BPP.Dataset.unique(),
                                value=df_APP_BPP.Dataset.unique(),
                                multi=False),

                            html.Label('Metric'),    
                            dcc.Dropdown(
                            id='metric-dropdown-app-bpp',
                            options = df_APP_BPP.Metric.unique(),
                            value= df_APP_BPP.Metric.unique(),
                            multi=False),

                            html.Label('Years'),
                            dcc.Dropdown(
                            id='year-dropdown-app-bpp',
                            options = df_APP_BPP.Year.unique(),
                            value= df_APP_BPP.Year.unique(),
                            ),
    
                            
                        ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                        html.Div(id='ppp-choices-container', children=[

                            html.Label('Dataset'),
                            dcc.Dropdown(
                            id='dataset-dropdown-ppp',
                            options = df_PPP.Dataset.unique(),
                            value=df_PPP.Dataset.unique(),
                            multi=False),

                            ## In the main distributing costs page, the accounting framework dropdown needs to be hidden when the PPP is not selected
                            html.Label('Accounting framework'),
                            dcc.Dropdown(
                                id='accounting-dropdown-ppp',
                                options = df_PPP.Accounting.unique(),
                                value=df_PPP.Accounting.unique(),
                                multi=False),


                            html.Label('Sector'),
                            dcc.RadioItems(id='sector-radio-all-or-single-ppp',
                                    #options = df.Sector.unique(),
                                    #value= df.Sector.unique())
                                    # These sector options are acting as placeholders, once the dataset is chosen, the options will update to relate to the dataset
                                    options=[{'label': i, 'value': i} for i in radio_sector_options],
                                    value=radio_sector_options[0],
                                    inline=True),

                            ### Put the following code inside a container, only to be displayed if the single sector option is ticked in the checklist
                            html.Div(id='single-sector-choices-container-ppp', children=[

                            html.Label('Single sector'),

                            dcc.Dropdown(id='sector-dropdown-ppp',
                                        #options = df.Sector.unique(),
                                        #value= df.Sector.unique())
                                        # These sector options are acting as placeholders, once the dataset is chosen, the options will update to relate to the dataset
                                        #options=[{'label':x, 'value':x} for x in all] + [{'label': 'Select all', 'value': 'all_values'}], 
                                        #value='all_values',  
                                        #multi=True),
                                        options = df_PPP.Sector.unique(),
                                        value=df_PPP.Sector.unique(),
                                        multi=False),

                            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                            ## In the main distributing costs page, the greenhouse gas dropdown needs to be hidden when the PPP is not selected
                            html.Label('Greenhouse gas'),
                            dcc.Dropdown(
                                id='ghg-dropdown-ppp',
                                options = df_PPP.Gas.unique(),
                                value=df_PPP.Gas.unique(),
                                multi=False),

                            html.Label('Metric'),    
                            dcc.Dropdown(
                            id='metric-dropdown-ppp',
                            options = df_PPP.Metric.unique(),
                            value= df_PPP.Metric.unique(),
                            multi=False),

                            html.Label('Years'),

                            ################### Three range slider containers beneath this point

                            html.Div(id='range-slider-container1-ppp', children=[ #Note this is the range slider for the Eora-26 dataset

                            dcc.RangeSlider(
                                1990, 2015, 1,
                                value=[1990, 2015],
                                id='time-interval-selector1-ppp',
                                marks={i: {'label': '{}'.format(i)} for i in range(1990, 2015, 5)},
                                tooltip={"placement": "bottom", "always_visible": True},
                                allowCross=False
                                # step=1,
                                )

                            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                            html.Div(id='range-slider-container2-ppp', children=[ #Note this is the range slider for the UNFCCC dataset

                            dcc.RangeSlider(
                                1990, 2020, 1,
                                value=[1990, 2020],
                                id='time-interval-selector2-ppp',
                                marks={i: {'label': '{}'.format(i)} for i in range(1990, 2020, 5)},
                                tooltip={"placement": "bottom", "always_visible": True},
                                allowCross=False
                                # step=1,
                                )

                            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                            html.Div(id='range-slider-container3-ppp', children=[ #Note this is the range slider for the CEDS, Houghton and Nassikas dataset

                            dcc.RangeSlider(
                                1850, 2014, step = None,
                                value=[1850, 1960],
                                id='time-interval-selector3-ppp',
                                # The below line gives the option to rotate text on the year range slider.
                                #marks={i: {'label': '{}'.format(i), "style": {"transform": "rotate(45deg)"}} for i in dates}, #for i in range(1850, 2014, 10)},
                                marks={i: {'label': '{}'.format(i)} for i in dates},
                                tooltip={"placement": "bottom", "always_visible": True},
                                allowCross=False
                                # step=1,
                                )

                            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                            ################### Three range slider containers above this point
                            

                        ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                        html.Label('Countries'),
                            dcc.RadioItems(id='country-radio-all-or-top-app-bpp',
                                    #options = df.Sector.unique(),
                                    #value= df.Sector.unique())
                                    # These sector options are acting as placeholders, once the dataset is chosen, the options will update to relate to the dataset
                                    options=radio_country_options,
                                    value=radio_country_options[0]), 

                            ### Put the following code inside a container, only to be displayed if the top 50 country option is ticked in the checklist
                            html.Div(id='top-country-choices-container-app-bpp', children=[

                                dcc.Dropdown(
                                    id='country-amount',
                                    options=[{'label': i, 'value': i} for i in number_of_countries.keys()],
                                    value=list(number_of_countries)[0]),

                            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                    #], style={'width': '50%'}),
                    ], id='left-container')
                ]
            ),
            html.Div(id='ppp-graph-container', children=[
                html.Div([          
                    dcc.Graph(
                    id='costs-graph-ppp',style={'padding': 10})
                ], id='right-container')
            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

            html.Div(id='app-bpp-graph-container', children=[
                html.Div([          
                    dcc.Graph(
                    id='costs-graph-app-bpp',style={'padding': 10})
                ], id='right-container')
            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

            html.Div(id='table-container-app-bpp', children=[
                html.Div([
                    dash_table.DataTable(
                        # style_data={
                        #     'whiteSpace': 'normal',
                        #     'height': 'auto', 
                        # },
                        columns = [{"name": i, "id": i} for i in columns_reordered_APP_BPP],
                        #data=df_APP_BPP[0:10].to_dict('records'),
                        data=df_APP_BPP.to_dict('records'),
                        style_header={
                                      'backgroundColor': '#609cd4', #'#e1e4eb',
                                      'fontWeight': 'bold',
                                      'align': 'center'},
                        style_cell={'fontSize':16, 'font-family':'Arial',
                                    'minWidth': '100px', 'width': '100px', 'maxWidth': '300px',
                                    'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'textAlign': 'left',},
                        id='table-app-bpp'),
                        
                ], id='tab-container', style={'padding':10})
            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback),

            html.Div(id='table-container-ppp', children=[
                html.Div([
                    dash_table.DataTable(
                        # style_data={
                        #     'whiteSpace': 'normal',
                        #     'height': 'auto', 
                        # },
                        columns = [{"name": i, "id": i} for i in columns_reordered_PPP],
                        #data=df_APP_BPP[0:10].to_dict('records'),
                        data=df_APP_BPP.to_dict('records'),
                        style_header={
                                      'backgroundColor': '#609cd4', #'#e1e4eb',
                                      'fontWeight': 'bold',
                                      'align': 'center'},
                        style_cell={'fontSize':16, 'font-family':'Arial',
                                    'minWidth': '100px', 'width': '100px', 'maxWidth': '300px',
                                    'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'textAlign': 'left',},
                        id='table-ppp'),
                        
                ], id='tab-container', style={'padding':10})
            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback)
                #], style= {'display': 'block'})

        ]
    )
])

### Making principle choice update dataset options for PPP
@callback(
    Output('dataset-dropdown-ppp', 'options'),
    Input('principle-dropdown', 'value')
    )

def set_datasets_option_for_ppp(principle_choice):
    dff= df_PPP.loc[df_PPP.Principle.apply(lambda x: x == principle_choice)]
    return [{'label': c, 'value': c} for c in sorted(dff.Dataset.unique())]

### Making principle choice update dataset options for APP and BPP
@callback(
    Output('dataset-dropdown-app-bpp', 'options'),
    Input('principle-dropdown', 'value')
    )

def set_datasets_option_for_app_bpp(principle_choice):
    dff= df_APP_BPP.loc[df_APP_BPP.Principle.apply(lambda x: x == principle_choice)]
    return [{'label': c, 'value': c} for c in sorted(dff.Dataset.unique())]

### Making dataset choice update accounting framework options for PPP
@callback(
    Output('accounting-dropdown-ppp', 'options'),
    Input('dataset-dropdown-ppp', 'value')
    #Input('principle-dropdown-ppp', 'value')
    )

def set_accounting_frameworks_options(dataset_choice):
    dff= df_PPP.loc[(df_PPP.Dataset.apply(lambda x: x == dataset_choice))]
    #if principle_choice == 'Polluter Pays':
    return [{'label': c, 'value': c} for c in sorted(dff.Accounting.unique())]
    #return dataset_choice

### Making dataset choice update sector options for PPP
@callback(
    Output('sector-dropdown-ppp', 'options'),
    Input('dataset-dropdown-ppp', 'value')
)

def set_sector_options(dataset_choice):
    dff= df_PPP.loc[df_PPP.Dataset.apply(lambda x: x == dataset_choice)]
    return [{'label': c, 'value': c} for c in sorted(dff.Sector.unique())]

################# Single sector choices container visibility state

@callback(
   Output('single-sector-choices-container-ppp', 'style'),
   Input('sector-radio-all-or-single-ppp', 'value')
)
def show_hide_single_sector_choices_container_ppp(visibility_state):
    if visibility_state == 'Single sector':
        return {'display': 'block'}
    return {'display': 'none'}

### Make principle choice and dataset choice update ghg options for PPP
@callback(
    Output('ghg-dropdown-ppp', 'options'),
    [Input('principle-dropdown', 'value'),
    Input('dataset-dropdown-ppp', 'value')
    ])

def set_ghg_options(principle_choice, dataset_choice):

    dff= df_PPP.loc[(df_PPP.Principle.apply(lambda x: x == principle_choice)) & (df_PPP.Dataset.apply(lambda x: x == dataset_choice))]
    return [{'label': c, 'value': c} for c in sorted(dff.Gas.unique())]

### Making principle choice and dataset choice update metric choice for PPP
@callback(
    Output('metric-dropdown-ppp', 'options'),
    [Input('principle-dropdown', 'value'),
     Input('dataset-dropdown-ppp', 'value')
    ])

def set_metrics_options_for_ppp(principle_choice, dataset_choice):
    dff = df_PPP.loc[df_PPP.Principle.apply(lambda x: x == principle_choice) & (df_PPP.Dataset.apply(lambda x: x == dataset_choice))]
    return [{'label': c, 'value': c} for c in sorted(dff.Metric.unique())]

### Making principle choice and dataset choice update metric choice for APP and BPP
@callback(
    Output('metric-dropdown-app-bpp', 'options'),
    Input('principle-dropdown', 'value'),
    Input('dataset-dropdown-app-bpp', 'value')
    )

def set_metrics_options_for_app_and_bpp(principle_choice, dataset_choice):
    dff = df_APP_BPP.loc[df_APP_BPP.Principle.apply(lambda x: x == principle_choice) & (df_APP_BPP.Dataset.apply(lambda x: x == dataset_choice))]
    return [{'label': c, 'value': c} for c in sorted(dff.Metric.unique())]

@callback(
    Output('year-dropdown-app-bpp', 'options'),
    [Input('principle-dropdown', 'value'),
    Input('dataset-dropdown-app-bpp', 'value'),
    Input('metric-dropdown-app-bpp', 'value')]
)

def set_years_options_from_metric_and_dataset_app_bpp(principle_choice, dataset_choice, metric_choice):
    dff= df_APP_BPP.loc[(df_APP_BPP.Dataset.apply(lambda x: x == dataset_choice)) & (df_APP_BPP.Principle.apply(lambda x: x == principle_choice)) & (df_APP_BPP.Metric.apply(lambda x: x == metric_choice))]
    return [{'label': c, 'value': c} for c in sorted(dff.Year.unique())]

@callback(
   Output('range-slider-container1-ppp', 'style'),
   Input('dataset-dropdown-ppp', 'value')
)
def show_hide_time_interval_selector_choices1(visibility_state):
    if (visibility_state == 'Eora-26'):
        return {'display': 'block'}
    return {'display': 'none'}

@callback(
   Output('range-slider-container2-ppp', 'style'),
   Input('dataset-dropdown-ppp', 'value')
)
def show_hide_time_interval_selector_choices2(visibility_state):
    if (visibility_state == 'UNFCCC'):
        return {'display': 'block'}
    return {'display': 'none'}

@callback(
   Output('range-slider-container3-ppp', 'style'),
   Input('dataset-dropdown-ppp', 'value')
)
def show_hide_time_interval_selector_choices3(visibility_state):
    if (visibility_state == 'CEDS, Houghton & Nassikas (2017) - All GHGs') | (visibility_state == 'CEDS, Houghton & Nassikas (2017)'):
        return {'display': 'block'}
    return {'display': 'none'}

###############################################

@callback(
   Output('app-bpp-choices-container', 'style'),
   Input('principle-dropdown', 'value')
)
def show_hide_app_bpp_choices(visibility_state):
    if visibility_state != 'Polluter Pays':
        return {'display': 'block'}
    return {'display': 'none'}

@callback(
   Output('ppp-choices-container', 'style'),
   Input('principle-dropdown', 'value')
)
def show_hide_ppp_choices(visibility_state):
    if visibility_state == 'Polluter Pays':
        return {'display': 'block'}
    return {'display': 'none'}

######################## Top 50 countries choices containers #########################

@callback(
   Output('top-country-choices-container-app-bpp', 'style'),
   Input('country-radio-all-or-top-app-bpp', 'value')
   #Input('top-50','value')
)
def show_hide_top_country_choices_container_app_bpp(visibility_state):
    if visibility_state == 'Some other number of countries':
        return {'display': 'block'}
    return {'display': 'none'}

####################################################################################

@callback(
   Output('table-container-app-bpp', 'style'),
   Input('principle-dropdown', 'value')
)
def show_hide_app_bpp_table_container(visibility_state):
    if visibility_state != 'Polluter Pays':
        return {'display': 'block'}
    return {'display': 'none'}

@callback(
   Output('table-container-ppp', 'style'),
   Input('principle-dropdown', 'value')
)
def show_hide_ppp_table_container(visibility_state):
    if visibility_state == 'Polluter Pays':
        return {'display': 'block'}
    return {'display': 'none'}
    
@callback(
   Output('ppp-graph-container', 'style'),
   Input('principle-dropdown', 'value')
)
def show_hide_element_ppp_graph(visibility_state):
    if visibility_state == 'Polluter Pays':
        return {'display': 'block'}
    return {'display': 'none'}
    
@callback(
   Output('app-bpp-graph-container', 'style'),
   Input('principle-dropdown', 'value')
)
def show_hide_element_app_bpp_graph(visibility_state):
    if visibility_state != 'Polluter Pays':
        return {'display': 'block'}
    return {'display': 'none'}

@callback(
    Output('costs-graph-ppp', 'figure'),
    Output('table-ppp', 'data'),
    [Input('principle-dropdown', 'value'),
    Input('dataset-dropdown-ppp', 'value'),
    Input('accounting-dropdown-ppp','value'),
    Input('sector-radio-all-or-single-ppp','value'),
    Input('sector-dropdown-ppp','value'),
    Input('ghg-dropdown-ppp','value'),
    Input('metric-dropdown-ppp', 'value'),
    #Input ('year-dropdown-ppp', 'value'),
    Input ('time-interval-selector1-ppp', 'value'),
    Input ('time-interval-selector2-ppp', 'value'),
    Input ('time-interval-selector3-ppp', 'value'),
    #Input ('country-dropdown-ppp', 'value'),
    Input('country-radio-all-or-top-app-bpp', 'value'),
    Input ('country-amount', 'value'),
    Input ('finance-amount', 'value')
    ])

def costs_PPP_graph(principle_choice, dataset_choice, accounting_choice, sector_all_choice, sector_single_choice, ghg_choice, metric_choice, time_interval_selector1, time_interval_selector2, time_interval_selector3, country_all_choice, country_amount, finance_goal): #countries_choice, finance_goal): #goal_choice): # ghg_choice, acc_fram_choice, principle_choice):

    if (dataset_choice == 'Eora-26'):
        time_interval_selector = time_interval_selector1
    elif (dataset_choice == 'UNFCCC'):
        time_interval_selector = time_interval_selector2
    else:
        time_interval_selector = time_interval_selector3


    year_range = list(range(time_interval_selector[0], time_interval_selector[1]+1))


    # Here we are checking whether all sectors have been selected or not, include all countries
    if (sector_all_choice == 'All sectors'):
        data = df_PPP.loc[(df_PPP.Principle.apply(lambda x: x == principle_choice)) & (df_PPP.Dataset.apply(lambda x: x == dataset_choice)) & (df_PPP.Accounting.apply(lambda x: x == accounting_choice)) & (df_PPP.Gas.apply(lambda x: x == ghg_choice)) & (df_PPP.Metric.apply(lambda x: x == metric_choice)) & (df_PPP.Year.isin(year_range))]
        data2 = data.reset_index()
    else:
        data = df_PPP.loc[(df_PPP.Principle.apply(lambda x: x == principle_choice)) & (df_PPP.Dataset.apply(lambda x: x == dataset_choice)) & (df_PPP.Accounting.apply(lambda x: x == accounting_choice)) & (df_PPP.Sector.apply(lambda x: x == sector_single_choice)) & (df_PPP.Gas.apply(lambda x: x == ghg_choice)) & (df_PPP.Metric.apply(lambda x: x == metric_choice)) & (df_PPP.Year.isin(year_range))]
        data2 = data.reset_index()

    print(data2)

    # In here you're going to need to sum greenhouse gas amounts over multiple years and add them together.
    # Do some kind of test. If there are multiple greenhouse gases and a metric has been selected, you need to do something different.

    finance_choice = costDictionary.get(finance_goal)

    # Calculations below this point relate to applying warming amounts
    if ((dataset_choice == 'CEDS, Houghton & Nassikas (2017) - All GHGs') | (dataset_choice == 'CEDS, Houghton & Nassikas (2017)')):
        start_year_choice = time_interval_selector[0]
        end_year_choice = time_interval_selector[1]
        #print('you are here')
        #print(start_year_choice)
        #print(end_year_choice)

        ey_data = data2.loc[(data2.Year.apply(lambda x: x == int(end_year_choice)))]
        sy_data = data2.loc[(data2.Year.apply(lambda x: x == int(start_year_choice)))]

        ey_data = ey_data.reset_index()
        ey_data = ey_data.fillna(0)
        sy_data = sy_data.reset_index()
        sy_data = sy_data.fillna(0)

        # Just add the greenhouse gas values together for now
        # ey_data = ey_data.groupby('Code')['Value'].sum()
        # sy_data = sy_data.groupby('Code')['Value'].sum()
        # print(sy_data)

        ey_data['Temp_difference'] = (ey_data['G_anthro'] - ey_data['Value']) - (sy_data['G_anthro'] - sy_data['Value'])
        ey_data['Finance_share'] = (ey_data['Temp_difference']/sum(ey_data['Temp_difference']))*finance_choice
        # If you wanted to look at warming from nitrous oxide as a proportion of total warming then you would need to have
        # a different line to the one directly above which would divide by the G_anthro difference between the start and end years.
        #ey_data['Finance_share'] = ey_data['Temp_difference']

        sorted_data = ey_data.sort_values('Finance_share', ascending=False)

        graph_title = f"Countries' fair shares of the {finance_goal} finance goal according to the {principle_choice} Principle based on {accounting_choice} warming in (\N{DEGREE SIGN}C) from {ghg_choice}<br>between {time_interval_selector[0]} and {time_interval_selector[1]}, with data from the {dataset_choice} dataset"

        if ((((dataset_choice == 'CEDS, Houghton & Nassikas (2017) - All GHGs') & (ghg_choice == 'All_GHGs'))) | ((dataset_choice == 'Eora-26') & (accounting_choice == 'Production-based')) | ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Total GHG emissions with LULUCF'))): 
            graph_title = f"(A)"
        elif ((((dataset_choice == 'CEDS, Houghton & Nassikas (2017)') & (ghg_choice == 'CO2'))) | ((dataset_choice == 'Eora-26') & (accounting_choice == 'Consumption-based')) | ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Total GHG emissions without LULUCF'))): 
            graph_title = f"(B)"
        elif (((dataset_choice == 'CEDS, Houghton & Nassikas (2017)') & (ghg_choice == 'CH4')) | ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Energy'))):  
            graph_title = f"(C)"
        #elif ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Waste')):
        #    graph_title = f"(C)"
        elif (((dataset_choice == 'CEDS, Houghton & Nassikas (2017)') & (ghg_choice == 'NOx')) | ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Industrial Processes and Product Use'))): 
            graph_title = f"(D)"
        #elif ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Industrial Processes and Product Use')):
        #    graph_title = f"(D)"
        elif ((dataset_choice == 'UNFCCC') & (ghg_choice == 'CH4')):
            graph_title = f"(E)"
        elif ((dataset_choice == 'UNFCCC') & (ghg_choice == 'N2O')):
            graph_title = f"(F)"    
        else:
            graph_title = f"(G)"

    else:
        data2 = data2.groupby(['Country','Code'])['Value'].sum().reset_index()
        data2['Finance_share'] = (data2['Value']/sum(data2['Value']))*finance_choice
        sorted_data = data2.sort_values('Finance_share', ascending=False)

        graph_title = f"Countries' fair shares of the {finance_goal} finance goal according to the {principle_choice} Principle based on {accounting_choice} emissions from {ghg_choice}<br>between {time_interval_selector[0]} and {time_interval_selector[1]}, with data from the {dataset_choice} dataset"

        if ((((dataset_choice == 'CEDS, Houghton & Nassikas (2017) - All GHGs') & (ghg_choice == 'All_GHGs'))) | ((dataset_choice == 'Eora-26') & (accounting_choice == 'Production-based')) | ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Total GHG emissions with LULUCF'))): 
            graph_title = f"(A)"
        elif ((((dataset_choice == 'CEDS, Houghton & Nassikas (2017)') & (ghg_choice == 'CO2'))) | ((dataset_choice == 'Eora-26') & (accounting_choice == 'Consumption-based')) | ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Total GHG emissions without LULUCF'))): 
            graph_title = f"(B)"
        elif (((dataset_choice == 'CEDS, Houghton & Nassikas (2017)') & (ghg_choice == 'CH4')) | ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Energy'))):  
            graph_title = f"(C)"
        #elif ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Waste')):
        #    graph_title = f"(C)"
        elif (((dataset_choice == 'CEDS, Houghton & Nassikas (2017)') & (ghg_choice == 'NOx')) | ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Industrial Processes and Product Use'))): 
            graph_title = f"(D)"
        #elif ((dataset_choice == 'UNFCCC') & (sector_single_choice == 'Industrial Processes and Product Use')):
        #    graph_title = f"(D)"
        elif ((dataset_choice == 'UNFCCC') & (ghg_choice == 'CH4')):
            graph_title = f"(E)"
        elif ((dataset_choice == 'UNFCCC') & (ghg_choice == 'N2O')):
            graph_title = f"(F)"    
        else:
            graph_title = f"(G)"

    print(sorted_data)

    if (country_all_choice != 'All countries'):
        country_amount_choice = number_of_countries.get(country_amount)
        sorted_data = sorted_data.head(country_amount_choice)

    color_discrete_sequence = ['#609cd4']*len(sorted_data)
    #fig = px.bar(sorted_data.sort_values('Value_2',ascending=False),

    

    fig = px.bar(sorted_data,
                 x='Code',
                 y='Finance_share',
                 #labels=["Country","Cost $US billions"],
                 title= graph_title,
                 labels=dict(x="Contribution US$"),
                 color=sorted_data['Code'],
                 color_discrete_sequence = color_discrete_sequence
                 )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(plot_bgcolor = "white")
    fig.update_layout(xaxis_title="Country code", yaxis_title="Cost (US$ billions)")

    data_for_table = sorted_data
    data_for_table['Finance_share'] = data_for_table['Finance_share']/1000000000

    data_for_table['Finance_share'] = data_for_table['Finance_share'].map('{:,.3f}'.format)
    data_for_table['Rank'] = range(1, len(data_for_table)+ 1)
    #print(data_for_table)

    data_for_table = data_for_table[['Rank','Country','Code','Finance_share']]
    #print(data_for_table)
    # data_for_table = data_for_table.rename(columns={'Code':'Country Code'}, inplace=True)
    # data_for_table = data_for_table.rename(columns={'Value':'Cost (US$)'}, inplace=True)
    #data_for_table = data_for_table[0:9]

    #return fig, data_for_table[0:10].to_dict('records')
    return fig, data_for_table.to_dict('records')


@callback(
    Output('costs-graph-app-bpp', 'figure'),
    Output('table-app-bpp','data'),
    [Input('principle-dropdown', 'value'),
    Input('dataset-dropdown-app-bpp', 'value'),
    Input('metric-dropdown-app-bpp', 'value'),
    Input ('year-dropdown-app-bpp', 'value'),
    Input('country-radio-all-or-top-app-bpp', 'value'),
    Input ('country-amount', 'value'),
    Input ('finance-amount', 'value')
    ])

def costs_APP_BPP_graph(principle_choice, dataset_choice, metric_choice, year_choice, country_all_choice, country_amount, finance_goal): #goal_choice): # ghg_choice, acc_fram_choice, principle_choice):

    full_data = df_APP_BPP.loc[(df_APP_BPP.Principle.apply(lambda x: x == principle_choice)) & (df_APP_BPP.Dataset.apply(lambda x: x == dataset_choice)) & (df_APP_BPP.Metric.apply(lambda x: x == metric_choice)) & (df_APP_BPP.Year.apply(lambda x: x == year_choice))]
    full_data = full_data.reset_index()
    full_data = full_data.fillna(0)
    total_value = sum(full_data['Value'])

    finance_choice = costDictionary.get(finance_goal)
    data2 = full_data
    data2['Value'] = (data2['Value']/total_value)*finance_choice
    data2 = data2.sort_values('Value',ascending=False)

    # Do a check here for if only one country has been selected
    # Here we are checking whether all sectors have been selected or not, for the selected country
    if (country_all_choice != 'All countries'):
        country_amount_choice = number_of_countries.get(country_amount)
        data2 = data2.head(country_amount_choice)
        data2 = data2.reset_index()
        data2 = data2.fillna(0)

    color_discrete_sequence = ['#609cd4']*len(data2)

    graph_title = f"Countries' fair shares of the {finance_goal} finance goal according to the {principle_choice} Principle based on {year_choice} {metric_choice} data from the {dataset_choice}"

    if (principle_choice == 'Ability to Pay'):
        if (metric_choice == 'GDP'): 
            graph_title = f"(A)"
        elif (metric_choice == 'GNI'):
            graph_title = f"(B)"
        elif (metric_choice == 'GDP per capita'):
            graph_title = f"(C)"
        elif (metric_choice == 'GNI per capita'):
            graph_title = f"(D)"
        else:
            graph_title = f"(E)"
    elif (principle_choice == 'Beneficiary Pays'):
        if ((metric_choice == 'Total wealth') & (year_choice == 1995)):
            graph_title = f"(A)"
        elif ((metric_choice == 'Total wealth') & (year_choice == 2018)):
            graph_title = f"(B)"
        elif ((metric_choice == 'Total wealth per capita') & (year_choice == 1995)):
            graph_title = f"(C)"
        elif ((metric_choice == 'Total wealth per capita') & (year_choice == 2018)):
            graph_title = f"(D)"
        else:
            graph_title = f"(E)"
    else:
        graph_title = graph_title

    fig = px.bar(data2,
                 x='Code',
                 y='Value',
                 title=graph_title,
                 labels=dict(x="Contribution US$"),
                 color=data2['Code'],
                 color_discrete_sequence = color_discrete_sequence,
                 )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(plot_bgcolor = "white")
    fig.update_layout(xaxis_title="Country code", yaxis_title="Cost (US$ billions)")

    
    data_for_table = data2
    data_for_table['Value'] = data_for_table['Value']/1000000000

    data_for_table['Value'] = data_for_table['Value'].map('{:,.3f}'.format)
    data_for_table['Rank'] = range(1, len(data_for_table)+ 1)
    #print(data_for_table)

    data_for_table = data_for_table[['Rank', 'Country', 'Code', 'Value']]
    # data_for_table = data_for_table.rename(columns={'Code':'Country Code'}, inplace=True)
    # data_for_table = data_for_table.rename(columns={'Value':'Cost (US$)'}, inplace=True)
    #data_for_table = data_for_table[0:9]
    #print(data_for_table[0:19])
    #return fig, data_for_table[0:10].to_dict('records')
    return fig, data_for_table.to_dict('records')
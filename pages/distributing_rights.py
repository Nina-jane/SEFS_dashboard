import dash
from dash import dcc, html, dash_table, callback, Input, Output
import pandas as pd
import plotly.express as px
import os
from dash.dependencies import Input, Output

dash.register_page(__name__)

thisPath = os.path.abspath(os.path.dirname(__file__))

# Note that the below dataset is same as the costs_principles_PPP.csv dataset.
df = pd.read_csv(os.path.join(thisPath, os.pardir,'rights_principles_ecpce_grand_for_SEFS_online.csv'), index_col=None, encoding='cp1252', low_memory=False)
df_future_pop_scenarios = pd.read_csv(os.path.join(thisPath, os.pardir,'rights_future_population_scenarios.csv'), index_col=None, encoding='cp1252', low_memory=False)
df_historical_pop_estimates = pd.read_csv(os.path.join(thisPath, os.pardir,'rights_historical_population_estimates.csv'), index_col=None, encoding='cp1252', low_memory=False)

rights_options = ['Emissions rights', 'Warming rights']

principle_options = ['Historical cumulative per cumulative capita emissions (HCPCCE)', 'Historical cumulative per cumulative capita warming (HCPCCW)',
                     'Equal cumulative per cumulative capita emissions (ECPCCE)', 'Equal cumulative per cumulative capita warming (ECPCCW)',
                      'Grandfathering emissions rights', 'Grandfathering warming rights']
                     #'Historical cumulative emissions', 'Historical cumulative warming']

principle_options2 = ['Historical cumulative per cumulative capita emissions (HCPCCE)', 'Historical cumulative per cumulative capita warming (HCPCCW)',
                      'Equal cumulative per cumulative capita emissions (ECPCCE)', 'Equal cumulative per cumulative capita warming (ECPCCW)',
                      'Grandfathering emissions rights', 'Grandfathering warming rights']
#                    'Grandfathering (emissions rights)', 'Grandfathering (warming rights)']
#['Equal cumulative per cumulative capita emissions (ECPCCE)', 'Equal cumulative per cumulative capita warming (ECPCCW)',

radio_country_options = ['All countries', 'Some other number of countries']
radio_sector_options = ['All sectors', 'Single sector']

number_of_countries = {
    "Top 10": 10,
    "Top 20": 20,
    "Top 50": 50,
    "Top 100": 100,
    "Bottom 10": 10,
    "Bottom 20": 20,
    "Bottom 50": 50,
    "Bottom 100": 100 
}

columns_reordered_rights = df[["Rank","Country", "Code", "Value"]]

date_marks_Eora = [1850, 1990, 2015, 2100]
dragable_range_Eora = [1990, 2015]

date_marks_UNFCCC = [1850, 1990, 2020, 2100]
dragable_range_UNFCCC = [1990, 2020]

date_marks_historical = [1850, 1990, 1960, 2014, 2100]
dragable_range_historical = [1850, 1990, 1960, 2014]

date_marks_future = [1850, 1990, 2015, 2050, 2100]
dragable_range_future = [1990, 2100]

country_highlight_options = df['Code'].unique()

layout = html.Div([
    html.Div(
        children=[
            html.Div(
                className="user-selections-party-p1",
                children=[
                    html.Div([
                        html.H1('RQ3: How warming (or emissions) rights ought to be distributed between countries?', style={'textAlign': 'left'}),
                        
                        # html.Label('Country'), #className="selector-def"),
                        # dcc.Dropdown(id='country-to-highlight',
                        #     options = ((((df.Code).dropna()).sort_values(ascending=True))).unique().astype(str),
                        #     value = ((((df.Code).dropna()).sort_values(ascending=True))).unique().astype(str)),

                        html.Label('Country to highlight'), #className="selector-def"),
                        dcc.Dropdown(id='country-highlight',
                                    options=[{'label': i, 'value': i} for i in country_highlight_options],
                                    value=country_highlight_options[28]), #73),

                        # Principle choice for historical graph
                        html.Label('Emissions rights or warming rights?'),
                        dcc.Dropdown(
                            id='type-of-rights-dropdown',
                            options=[{'label': i, 'value': i} for i in rights_options],
                            value=rights_options[0], # could change the above to available_years_budget
                            searchable=False
                        ),

                        # Principle choice for historical graph
                        html.Label('Graph 1 choice'),
                        dcc.Dropdown(
                            id='principle-dropdown',
                            options=[{'label': i, 'value': i} for i in principle_options],
                            value=principle_options[0], # could change the above to available_years_budget
                            searchable=False
                        ),

                        # Principle choice for future rights graph
                        html.Label('Graph 2 choice'),
                        dcc.Dropdown(
                            id='principle-dropdown2',
                            options=[{'label': i, 'value': i} for i in principle_options2],
                            value=principle_options2[0], # could change the above to available_years_budget
                            searchable=False
                        ),

                        html.Div(id='rights-choices-container', children=[                      
                            html.Label('Dataset'),
                            dcc.Dropdown(
                                id='dataset-dropdown-rights',
                                options = ((((df.Dataset).dropna()).sort_values(ascending=True))).unique().astype(str),
                                value = ((((df.Dataset).dropna()).sort_values(ascending=True))).unique().astype(str)
                            ),
                            
                            ## Copied from distributing costs page
                            html.Label('Accounting framework'),
                            dcc.Dropdown(
                                id='accounting-dropdown-rights',
                                options = ((((df.Accounting).dropna()).sort_values(ascending=True))).unique().astype(str), #(df.Accounting).dropna().unique(), 
                                value = ((((df.Accounting).dropna()).sort_values(ascending=True))).unique().astype(str), #(df.Accounting).dropna().unique(),    #(df.Accounting.dropna()).unique(),
                                multi=False),

                            html.Label('Sector'),
                            dcc.RadioItems(id='sector-radio-all-or-single-rights',
                                    options=[{'label': i, 'value': i} for i in radio_sector_options],
                                    value=radio_sector_options[0],
                                    inline=True),

                            ### Put the following code inside a container, only to be displayed if the single sector option is ticked in the checklist
                            html.Div(id='single-sector-choices-container-rights', children=[

                            html.Label('Single sector'),

                            dcc.Dropdown(id='sector-dropdown-rights',
                                        options = df.Sector.unique(),
                                        value=df.Sector.unique(),
                                        multi=False),

                            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                            html.Label('Greenhouse gas'),
                            dcc.Dropdown(
                                id='ghg-dropdown-rights',
                                options = df.Gas.unique(),
                                value = df.Gas.unique(),
                                multi=False),

                            html.Label('Metric'),
                            dcc.Dropdown(
                                id='metric-dropdown-rights',
                                options = ((((df.Metric).dropna()).sort_values(ascending=True))).unique().astype(str),
                                value = ((((df.Metric).dropna()).sort_values(ascending=True))).unique().astype(str)  
                            ),

                            ### Adding the below code back in now because have got the ECPCE working like Grandfathering
                            html.Label('Historical population dataset'),
                            dcc.Dropdown(
                                id='dataset2-dropdown-rights',
                                options = ((((df_future_pop_scenarios.Population_dataset).dropna()).sort_values(ascending=True))).unique().astype(str), 
                                value = ((((df_future_pop_scenarios.Population_dataset).dropna()).sort_values(ascending=True))).unique().astype(str) 
                            ),
                            html.Label('Population growth scenario out to 2050'),
                            dcc.Dropdown(
                                id='pop-growth-scenario-dropdown-rights',
                                #options = df.iloc[:,12].unique(),
                                #value= df.iloc[:,12].unique()[0] #Don't necessarily have to specify this, you could have a test in here to avoid the division by zero error
                                #options = pop_scenario_options,
                                #value = pop_scenario_options[0]
                                options = ((((df_future_pop_scenarios.Pop_scenario).dropna()).sort_values(ascending=True))).unique().astype(str),
                                value = ((((df_future_pop_scenarios.Pop_scenario).dropna()).sort_values(ascending=True))).unique().astype(str) 
                            ),

                            html.Label('Historical emissions/warming range'),

                            ################### Three range slider containers beneath this point

                            html.Div(id='range-slider-container1-rights', children=[ #Note this is the range slider for the Eora-26 dataset

                                dcc.RangeSlider(
                                    1850, 2100, step=None,
                                    value=[1990, 2015],
                                    drag_value=dragable_range_Eora,
                                    id='time-interval-selector1-rights',
                                    marks={i: {'label': '{}'.format(i)} for i in date_marks_Eora}, #range(1990, 2015, 5)},
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    allowCross=False
                                    # step=1,
                                    )

                            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                            html.Div(id='range-slider-container2-rights', children=[ #Note this is the range slider for the UNFCCC dataset

                                dcc.RangeSlider(
                                    1850, 2100, step=None,
                                    value=[1990, 2020],
                                    drag_value=dragable_range_UNFCCC,
                                    id='time-interval-selector2-rights',
                                    marks={i: {'label': '{}'.format(i)} for i in date_marks_UNFCCC}, #range(1990, 2020, 5)},
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    allowCross=False
                                    # step=1,
                                    )

                            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                            html.Div(id='range-slider-container3-rights', children=[ #Note this is the range slider for the CEDS, Houghton and Nassikas dataset

                                dcc.RangeSlider(
                                    1850, 2100, step = None,
                                    value=[1850, 2014],
                                    drag_value=dragable_range_historical,
                                    id='time-interval-selector3-rights',
                                    # The below line gives the option to rotate text on the year range slider.
                                    #marks={i: {'label': '{}'.format(i), "style": {"transform": "rotate(45deg)"}} for i in dates}, #for i in range(1850, 2014, 10)},
                                    marks={i: {'label': '{}'.format(i)} for i in date_marks_historical},
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    allowCross=False
                                    # step=1,
                                    )

                            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                            ################### Three range slider containers above this point
                            

                            #], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                            html.Label('Emissions/warming budget range'),
                                dcc.RangeSlider(
                                1850, 2100, step = 1,
                                value=[2015,2050],
                                drag_value=dragable_range_future,
                                id='time-interval-selector-rights-future',
                                #marks={i: {'label': '{}'.format(i)} for i in range(min(df.Year.unique()), max(df.Year.unique()), 5)},
                                marks={i: {'label': '{}'.format(i)} for i in date_marks_future},
                                tooltip={"placement": "bottom", "always_visible": True},
                                allowCross=False
                                ),

                            html.Label('Countries'),
                            dcc.RadioItems(id='country-radio-all-or-top-rights',
                                    #options = df.Sector.unique(),
                                    #value= df.Sector.unique())
                                    # These sector options are acting as placeholders, once the dataset is chosen, the options will update to relate to the dataset
                                    options=radio_country_options,
                                    value=radio_country_options[0]), 

                            ### Put the following code inside a container, only to be displayed if the top 50 country option is ticked in the checklist
                            html.Div(id='top-country-choices-container-rights', children=[

                                dcc.Dropdown(
                                    id='country-amount',
                                    options=[{'label': i, 'value': i} for i in number_of_countries.keys()],
                                    value=list(number_of_countries)[0]),

                            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                        ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                    ],id='left-container')
                ]
            ),

            html.Div(id='rights-graph-container', children=[
                ### First historical use/share graph
                html.Div([
                    dcc.Graph(
                    id='historical-use-graph',style={'padding': 10})
                    ], id='right-container'),

            # ### Second future rights graph
                html.Div([
                    dcc.Graph(
                    id='rights-to-future-budget-graph',style={'padding': 10})
                    ], id='right-container')
            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

            # html.Div(id='table-container-rights', children=[
            #     html.Div([
            #         dash_table.DataTable(
            #             # style_data={
            #             #     'whiteSpace': 'normal',
            #             #     'height': 'auto', 
            #             # },
            #             columns = [{"name": i, "id": i} for i in columns_reordered_rights],
            #             #data=df_APP_BPP[0:10].to_dict('records'),
            #             data=df.to_dict('records'),
            #             style_header={
            #                           'backgroundColor': '#609cd4', #'#e1e4eb',
            #                           'fontWeight': 'bold',
            #                           'align': 'center'},
            #             style_cell={'fontSize':16, 'font-family':'Arial',
            #                         'minWidth': '100px', 'width': '100px', 'maxWidth': '300px',
            #                         'overflow': 'hidden',
            #                         'textOverflow': 'ellipsis',
            #                         'textAlign': 'left',},
            #             id='table-rights'),
                        
            #     ], id='table-container', style={'padding':10})
            # ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback)
        ])
])

### Have a bunch of callbacks here

# ### Making rights choice update principle-dropdown
@callback(
   Output('principle-dropdown', 'options'),
   Input('type-of-rights-dropdown', 'value')
   )

def set_principles_options(rights_choice):
    if "Warming" in rights_choice:
       new_principle_options = [x for x in principle_options if "warming" in x]
    else:
       new_principle_options = [x for x in principle_options if "emissions" in x]  
    return new_principle_options

@callback(
   Output('principle-dropdown2', 'options'),
   Input('type-of-rights-dropdown', 'value')
   )

def set_principles_options(rights_choice):
    if "Warming" in rights_choice:
       new_principle_options = [x for x in principle_options if "warming" in x]
    else:
       new_principle_options = [x for x in principle_options if "emissions" in x]  
    return new_principle_options

### Making principle choice update dataset-dropdown-rights
@callback(
    Output('dataset-dropdown-rights', 'options'),
    Input('principle-dropdown', 'value')
    )

def set_datasets_options(principle_choice):
    if ("warming" in principle_choice):
       dataset_types = ['CEDS, Houghton & Nassikas (2017)', 'CEDS, Houghton & Nassikas (2017) - All GHGs']
    else:
       dataset_types = ['Eora-26', 'UNFCCC']
    
    dff= df.loc[(df.Dataset.isin(dataset_types))]
    return [{'label': c, 'value': c} for c in (((dff.Dataset).dropna()).sort_values(ascending=True)).unique().astype(str)]
    
    #dff= df.loc[df.Rights.apply(lambda x: x == rights_choice)]
    #return [{'label': c, 'value': c} for c in (((dff.Dataset).dropna()).sort_values(ascending=True)).unique().astype(str)]

### Making dataset1 choice update accounting framework options for ECPCE
@callback(
    Output('accounting-dropdown-rights', 'options'),
    Input('dataset-dropdown-rights', 'value')
    )

def set_accounting_frameworks_options_rights(dataset_choice):
    dff= df.loc[(df.Dataset.apply(lambda x: x == dataset_choice))]
    return [{'label': c, 'value': c} for c in (((dff.Accounting).dropna()).sort_values(ascending=True)).unique().astype(str)]

### Making dataset1 choice update sector options for ECPCE
@callback(
    Output('sector-dropdown-rights', 'options'),
    Input('dataset-dropdown-rights', 'value')
)

def set_sector_options_rights(dataset_choice):
    dff= df.loc[df.Dataset.apply(lambda x: x == dataset_choice)]
    return [{'label': c, 'value': c} for c in ((((dff.Sector).dropna()).sort_values(ascending=True))).unique().astype(str)]

################# Single sector choices container visibility state

@callback(
   Output('single-sector-choices-container-rights', 'style'),
   Input('sector-radio-all-or-single-rights', 'value')
)
def show_hide_single_sector_choices_container_ppp(visibility_state):
    if visibility_state == 'Single sector':
        return {'display': 'block'}
    return {'display': 'none'}

####################################################################

### Making dataset choice update ghg options for ECPCE (used to be dataset when I was operationalising the PPP)
@callback(
    Output('ghg-dropdown-rights', 'options'),
    Input('dataset-dropdown-rights', 'value')
    #Input('sector-dropdown-rights', 'value') <- I commented this out as it is not longer needed and in fact it only confuses things and makes them less correct.
    )

def set_ghg_options_for_rights(dataset_choice):
    dff= df.loc[(df.Dataset.apply(lambda x: x == dataset_choice))]
    return [{'label': c, 'value': c} for c in sorted(dff.Gas.unique())]

### Making dataset choice update metric choice for ECPCE
@callback(
    Output('metric-dropdown-rights', 'options'),
    #Input('principle-dropdown', 'value'),
    Input('dataset-dropdown-rights', 'value')
    #Input('sector-dropdown-rights', 'value') <- I commented this out as it is not longer needed and in fact it only confuses things and makes them less correct.
    )

def set_metrics_options_for_rights(dataset_choice):
    dff = df.loc[(df.Dataset.apply(lambda x: x == dataset_choice))]
    return [{'label': c, 'value': c} for c in sorted(dff.Metric.unique())]
    # dff = df.loc[(df.Dataset.apply(lambda x: x == dataset_choice)) & (df.Sector.isin(sector_choice))] 
    # return [{'label': c, 'value': c} for c in ((((dff.Metric).dropna()).sort_values(ascending=True))).unique().astype(str)]

### Making metric choice, dataset1 choice and year choice update countries options for ECPCE
# @callback(
#     Output('country-dropdown-ECPCE', 'options'),
#     Input('metric-dropdown-ECPCE', 'value'),
#     Input('dataset-dropdown-rights', 'value')
#     #Input('time-interval-selector-rights-ECPCE', 'value')
# )
# # Note in the below one I am using the population data for the ECPCE
# def set_countries_options_from_metric_and_dataset_ECPCE(metric_choice, dataset_choice): #, year_choice):
#     dff= df.loc[df.Metric.apply(lambda x: x == metric_choice) & (df.Dataset.apply(lambda x: x == dataset_choice))] #& (df.Year.apply(lambda x: x == year_choice))]
#     return [{'label': c, 'value': c} for c in sorted(dff.Country.unique())]

######################## Callbacks to show and hide specific options for the different principles (in their containers) ########################

@callback(
  Output('rights-choices-container', 'style'),
  Input('principle-dropdown', 'value')
)
def show_hide_rights_choices(visibility_state):
   if visibility_state != 'Grandfathering':
       return {'display': 'block'}
   return {'display': 'none'}

# @callback(
#    Output('grand-choices-container', 'style'),
#    Input('principle-dropdown', 'value')
# )
# def show_hide_grand_choices(visibility_state):
#     if visibility_state == 'Grandfathering':
#         return {'display': 'block'}
#     return {'display': 'none'}

######################## Top 50 countries choices containers #########################

@callback(
   Output('top-country-choices-container-rights', 'style'),
   Input('country-radio-all-or-top-rights', 'value')
   #Input('top-50','value')
)
def show_hide_top_country_choices_container_app_bpp(visibility_state):
    if visibility_state == 'Some other number of countries':
        return {'display': 'block'}
    return {'display': 'none'}

######################## Callbacks to highlight a country's bar orange ###############

# @callback(
#    Output('country-highlight-rights', 'options'),
#    Input('country-radio-all-or-top-rights', 'value')
# )
# def highlight_single_country(countries_subset_choice):
#     dff = df.loc[(df.Country.apply(lambda x: x == countries_subset_choice))]
#     return [{'label': c, 'value': c} for c in ((((dff.Country).dropna()).sort_values(ascending=True))).unique().astype(str)]
#     #return [{'label': c, 'value': c} for c in sorted(dff.Country.unique())]

######################## Callbacks to show and hide the Range Sliders ################

@callback(
   Output('range-slider-container1-rights', 'style'),
   Input('dataset-dropdown-rights', 'value')
)
def show_hide_time_interval_selector_choices1(visibility_state):
    if (visibility_state == 'Eora-26'):
        return {'display': 'block'}
    return {'display': 'none'}

@callback(
   Output('range-slider-container2-rights', 'style'),
   Input('dataset-dropdown-rights', 'value')
)
def show_hide_time_interval_selector_choices2(visibility_state):
    if (visibility_state == 'UNFCCC'):
        return {'display': 'block'}
    return {'display': 'none'}

@callback(
   Output('range-slider-container3-rights', 'style'),
   Input('dataset-dropdown-rights', 'value')
)
def show_hide_time_interval_selector_choices3(visibility_state):
    if (visibility_state == 'CEDS, Houghton & Nassikas (2017) - All GHGs') | (visibility_state == 'CEDS, Houghton & Nassikas (2017)'):
        return {'display': 'block'}
    return {'display': 'none'}

####### Callbacks to show and hide the table (in its container) ############

# @callback(
#    Output('table-container-rights', 'style'),
#    Input('principle-dropdown', 'value')
# )
# def show_hide_app_bpp_table_container(visibility_state):
#     if (visibility_state != 'Grandfathering (warming rights)') | (visibility_state != 'Grandfathering (emissions rights)'):
#         return {'display': 'block'}
#     return {'display': 'none'}

### Create a graph here, with various inputs

## Activate the following callback update ###
@callback(
    Output('historical-use-graph', 'figure'),
    #Output('table-rights','data'),
    [Input('country-highlight', 'value'),
    Input('principle-dropdown', 'value'),
    Input('dataset-dropdown-rights', 'value'),
    Input('accounting-dropdown-rights','value'),
    Input('sector-radio-all-or-single-rights','value'),
    Input('sector-dropdown-rights','value'),
    Input('ghg-dropdown-rights','value'),
    Input('metric-dropdown-rights', 'value'),
    Input ('time-interval-selector1-rights', 'value'),
    Input ('time-interval-selector2-rights', 'value'),
    Input ('time-interval-selector3-rights', 'value'),
    Input ('country-radio-all-or-top-rights', 'value'),
    Input ('country-amount', 'value'),
    Input('pop-growth-scenario-dropdown-rights', 'value'),
    Input('time-interval-selector-rights-future', 'value'),
    #Input('country-to-highlight','value'),
    ])

def historical_use_graph(country_to_highlight,principle_choice, dataset_choice, accounting_choice, sector_all_choice, sector_single_choice, ghg_choice, metric_choice, time_interval_selector1_rights, time_interval_selector2_rights, time_interval_selector3_rights, country_all_choice, country_amount, pop_growth_scenario, time_interval_selector_pop): #country_to_highlight):

    if (dataset_choice == 'Eora-26'):
        time_interval_selector_rights = time_interval_selector1_rights
    elif (dataset_choice == 'UNFCCC'):
        time_interval_selector_rights = time_interval_selector2_rights
    else:
        time_interval_selector_rights = time_interval_selector3_rights

    year_range = list(range(time_interval_selector_rights[0], time_interval_selector_rights[1]+1))

    # Here we are checking whether all sectors have been selected or not, include all countries
    if (sector_all_choice == 'All sectors'):
        data = df.loc[(df.Dataset.apply(lambda x: x == dataset_choice)) & (df.Accounting.apply(lambda x: x == accounting_choice)) & (df.Gas.apply(lambda x: x == ghg_choice)) & (df.Metric.apply(lambda x: x == metric_choice)) & (df.Year.isin(year_range))]
        data2 = data.reset_index()
    else:
        data = df.loc[(df.Dataset.apply(lambda x: x == dataset_choice)) & (df.Accounting.apply(lambda x: x == accounting_choice)) & (df.Sector.apply(lambda x: x == sector_single_choice)) & (df.Gas.apply(lambda x: x == ghg_choice)) & (df.Metric.apply(lambda x: x == metric_choice)) & (df.Year.isin(year_range))]
        data2 = data.reset_index()

    ################################################################################################
        
    finance_choice = float(100)

    start_year_choice = time_interval_selector_rights[0]
    end_year_choice = time_interval_selector_rights[1]

    ey_data = data2.loc[(data2.Year.apply(lambda x: x == int(end_year_choice)))]
    sy_data = data2.loc[(data2.Year.apply(lambda x: x == int(start_year_choice)))]

    ey_data = ey_data.reset_index()
    ey_data = ey_data.fillna(0)
    sy_data = sy_data.reset_index()
    sy_data = sy_data.fillna(0)

    # Getting historical population numbers
    historical_populations = df_historical_pop_estimates.loc[(df_historical_pop_estimates.Year.isin(year_range))]
    historical_populations = historical_populations.reset_index()
    historical_person_years = historical_populations.groupby(['Country','Code'])['Historical_population_estimate'].sum().reset_index()
    historical_person_years = historical_person_years.rename(columns={'Historical_population_estimate':'Historical_person_years'})

    # First step: calculate warming amounts, for those principles that need it
    if ("warming" in principle_choice):
    # Calculations below this point relate to applying warming amounts
        
        ey_data['Temp_difference'] = (ey_data['G_anthro'] - ey_data['Value']) - (sy_data['G_anthro'] - sy_data['Value'])
        ey_data['Finance_share'] = (ey_data['Temp_difference']/sum(ey_data['Temp_difference']))*finance_choice
        # If you wanted to look at warming from nitrous oxide as a proportion of total warming then you would need to have
        # a different line to the one directly above which would divide by the G_anthro difference between the start and end years.
        #ey_data['Finance_share'] = ey_data['Temp_difference']

        sorted_data = ey_data.sort_values('Temp_difference', ascending=False)
        # IT MIGHT MAKE SENSE TO SWITCH FROM FINANCE SHARE TO TEMP DIFFERENCE
        #sorted_data = ey_data.sort_values('Temp_difference', ascending=False)

        #y_axis_data = 'Temp_difference'
        graph_title = f"Countries' historical shares of warming (in \N{DEGREE SIGN}C) from {ghg_choice} emissions between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} datasets"
        
    else:
        # Just add the greenhouse gas values together for now
        # ey_data = ey_data.groupby('Code')['Value'].sum()
        # sy_data = sy_data.groupby('Code')['Value'].sum()
        # print(sy_data)
        
        data2 = data2.groupby(['Country','Code'])['Value'].sum().reset_index()
        data2['Finance_share'] = (data2['Value']/sum(data2['Value']))*finance_choice
        #sorted_data = data2.sort_values('Temp_difference', ascending=False)
        sorted_data = data2.sort_values('Value', ascending=False)
        
        #y_axis_data = 'Value'
        graph_title = f"Countries' historical shares of {ghg_choice} emissions (in kt) between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} dataset"

    #### Have added in new code here!!!    
    # Second step: calculate per capita amounts, for those principles that need it
    if ("HCPCCW" in principle_choice): # This is HCPCCW
        # ####### Second step is to join the warming/emissions datasets with the cumulative capita dataset, based on the country codes
        # This means then that the 'sorted data' and 'y' input values in the code to make the graph below should be different.
        data_with_person_years = sorted_data.merge(historical_person_years[['Code','Historical_person_years']],left_on='Code', right_on='Code')
        #### Check if a per capita principle has been selected. If one has, then calculate the number of cumulative person years
        data_with_person_years['Historical_per_capita'] = data_with_person_years['Temp_difference']/data_with_person_years['Historical_person_years']
        data_with_person_years = data_with_person_years.sort_values('Historical_per_capita', ascending=False)
        sorted_data = data_with_person_years
        y_axis_data = 'Historical_per_capita'
        graph_title = f"Countries' cumulative historical per cumulative capita warming (in \N{DEGREE SIGN}C) from {ghg_choice} emissions between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} datasets"
        # print("HPCCW")
        # print(len(sorted_data))

        #graph_title = f"(C)"
    
    elif ("HCPCCE" in principle_choice): # This is HCPCCE
        data_with_person_years = sorted_data.merge(historical_person_years[['Code','Historical_person_years']],left_on='Code', right_on='Code')
        #### Check if a per capita principle has been selected. If one has, then calculate the number of cumulative person years
        data_with_person_years['Historical_per_capita'] = data_with_person_years['Value']/data_with_person_years['Historical_person_years']
        data_with_person_years = data_with_person_years.sort_values('Historical_per_capita', ascending=False)
        sorted_data = data_with_person_years
        y_axis_data = 'Historical_per_capita'
        graph_title = f"Countries' cumulative historical per cumulative capita {ghg_choice} emissions (in kt) between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} dataset"
        # print("HPCCE")
        # print(len(sorted_data))
    
    elif ("ECPCCW" in principle_choice): # This is ECPCCW

        ##### This is old code beneath this point

        # # ####### Second step is to join the warming/emissions datasets with the cumulative capita dataset, based on the country codes
        # # This means then that the 'sorted data' and 'y' input values in the code to make the graph below should be different.
        # data_with_person_years = sorted_data.merge(historical_person_years[['Code','Historical_person_years']],left_on='Code', right_on='Code')
        # #### Check if a per capita principle has been selected. If one has, then calculate the number of cumulative person years
        # data_with_person_years['Historical_per_capita'] = data_with_person_years['Temp_difference']/data_with_person_years['Historical_person_years']
        # data_with_person_years = data_with_person_years.sort_values('Historical_per_capita', ascending=False)
        # sorted_data = data_with_person_years
        
        # y_axis_data = 'Historical_per_capita'
        # graph_title = f"Countries' historical per capita warming (in \N{DEGREE SIGN}C) from {ghg_choice} emissions between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} datasets"
        # #print("HPCCW")
        # #print(len(sorted_data))

        ##### This is old code above this point

        ######## THIS IS WHERE YOU WANT TO ADD THE CALCULATIONS FOR FUTURE PER CAPITA RIGHTS. BE CAREFUL WITH SMALL NUMBERS HERE
        # 0. Get year range for future population.
        year_range_for_future_population = list(range(time_interval_selector_pop[0], time_interval_selector_pop[1]+1))
        
        # 1. Get future population datasets
        future_populations = df_future_pop_scenarios.loc[(df_future_pop_scenarios.Pop_scenario.apply(lambda x: x == pop_growth_scenario)) & (df_future_pop_scenarios.Year.isin(year_range_for_future_population))]
        future_populations.reset_index()
        future_person_years = future_populations.groupby(['Country','Code'])['Population'].sum().reset_index()
        future_person_years = future_person_years.rename(columns={'Population':'Future_person_years'})

        # 2. Merge historical population and future population datasets
        df_with_future_person_years = historical_person_years.merge(future_person_years[['Code','Future_person_years']],left_on='Code', right_on='Code') #.drop('Code',axis='columns')
        #print('df with future person years')
        #print(df_with_future_person_years)
        # 2.5 Merge warming information with population datasets (historical and future)
        df_with_all_info = sorted_data.merge(df_with_future_person_years[['Code', 'Historical_person_years','Future_person_years']],left_on='Code', right_on='Code')
        #print('df with all info')
        #print(df_with_all_info)

        # 3. Calculate the total person years
        df_with_all_info['Total_person_years'] = df_with_all_info['Historical_person_years'] + df_with_all_info['Future_person_years']

        # 4. Calculate:
        # - historical warming
        world_historical_warming = df_with_all_info['Temp_difference'].sum() #<- This is generating the current Temp_difference error
        # - world warming limit
        world_warming_limit = 1.1*world_historical_warming
        # - world historical person years
        world_historical_person_years = df_with_all_info['Historical_person_years'].sum()
        # - world future person years
        world_future_person_years = df_with_all_info['Future_person_years'].sum()
        # - world total person years
        world_total_person_years = df_with_all_info['Total_person_years'].sum()
        # - world equal cumulative capita amount of warming
        world_equal_cumulative_capita_amount_warming = world_warming_limit/world_total_person_years
        # - cumulative capita warming
        cumulative_capita_warming = world_historical_warming/world_total_person_years

        df_with_all_info['EPC_fair_share'] = df_with_all_info['Total_person_years']*world_equal_cumulative_capita_amount_warming
        df_with_all_info['EPC_budget'] = df_with_all_info['EPC_fair_share'].sub(df_with_all_info['Temp_difference'])

        sorted_data = df_with_all_info.sort_values('EPC_budget', ascending=False)
        y_axis_data = 'EPC_budget'
        graph_title = f"Countries' equal per capita shares of warming (in \N{DEGREE SIGN}C) based upon historical {ghg_choice} emissions between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, under the {accounting_choice}<br>accounting framework with data from the {dataset_choice} datasets"

        #graph_title = f"(A)"

    elif ("ECPCCE" in principle_choice): # This is ECPCCE
        
        ##### This is old code beneath this point

        # data_with_person_years = sorted_data.merge(historical_person_years[['Code','Historical_person_years']],left_on='Code', right_on='Code')
        # #### Check if a per capita principle has been selected. If one has, then calculate the number of cumulative person years
        # data_with_person_years['Historical_per_capita'] = data_with_person_years['Value']/data_with_person_years['Historical_person_years']
        # data_with_person_years = data_with_person_years.sort_values('Historical_per_capita', ascending=False)
        # sorted_data = data_with_person_years
        # y_axis_data = 'Historical_per_capita'
        # graph_title = f"Countries' historical per capita {ghg_choice} emissions (in kt) between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice}<br>accounting framework with data from the {dataset_choice} dataset"
        # #print("HPCCE")
        # #print(len(sorted_data))

        ##### This is old code above this point

        ######## THIS IS WHERE YOU WANT TO ADD THE CALCULATIONS FOR FUTURE PER CAPITA RIGHTS. BE CAREFUL WITH SMALL NUMBERS HERE
        # 0. Get year range for future population.
        year_range_for_future_population = list(range(time_interval_selector_pop[0], time_interval_selector_pop[1]+1))
        
        # 1. Get future population datasets
        future_populations = df_future_pop_scenarios.loc[(df_future_pop_scenarios.Pop_scenario.apply(lambda x: x == pop_growth_scenario)) & (df_future_pop_scenarios.Year.isin(year_range_for_future_population))]
        future_populations.reset_index()
        future_person_years = future_populations.groupby(['Country','Code'])['Population'].sum().reset_index()
        future_person_years = future_person_years.rename(columns={'Population':'Future_person_years'})

        # 2. Merge historical population and future population datasets
        df_with_future_person_years = historical_person_years.merge(future_person_years[['Code','Future_person_years']],left_on='Code', right_on='Code') #.drop('Code',axis='columns')
        #print('df with future person years')
        #print(df_with_future_person_years)
        # 2.5 Merge warming information with population datasets (historical and future)
        df_with_all_info = sorted_data.merge(df_with_future_person_years[['Code', 'Historical_person_years','Future_person_years']],left_on='Code', right_on='Code')
        #print('df with all info')
        #print(df_with_all_info)

        # 3. Calculate the total person years
        df_with_all_info['Total_person_years'] = df_with_all_info['Historical_person_years'] + df_with_all_info['Future_person_years']

        # 4. Calculate:
        # - historical warming
        world_historical_warming = df_with_all_info['Value'].sum() #<- This (when it used to be Temp_difference instead of Value) was generating the current Temp_difference error
        # - world warming limit
        world_warming_limit = 1.1*world_historical_warming
        # - world historical person years
        world_historical_person_years = df_with_all_info['Historical_person_years'].sum()
        # - world future person years
        world_future_person_years = df_with_all_info['Future_person_years'].sum()
        # - world total person years
        world_total_person_years = df_with_all_info['Total_person_years'].sum()
        # - world equal cumulative capita amount of warming
        world_equal_cumulative_capita_amount_warming = world_warming_limit/world_total_person_years
        # - cumulative capita warming
        cumulative_capita_warming = world_historical_warming/world_total_person_years

        df_with_all_info['EPC_fair_share'] = df_with_all_info['Total_person_years']*world_equal_cumulative_capita_amount_warming
        df_with_all_info['EPC_budget'] = df_with_all_info['EPC_fair_share'].sub(df_with_all_info['Value'])

        sorted_data = df_with_all_info.sort_values('EPC_budget', ascending=False)

        y_axis_data = 'EPC_budget'
        graph_title = f"Countries' equal per capita shares of {ghg_choice} emissions based upon historical {ghg_choice} emissions (in kt) between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, under the {accounting_choice}<br>accounting framework with data from the {dataset_choice} dataset"

    elif (("Grandfathering" in principle_choice) & ("warming" in principle_choice)): # This is Grandfathering (warming rights)
        sorted_data = sorted_data
        y_axis_data = 'Temp_difference'
        graph_title = f"Countries' historical warming (in \N{DEGREE SIGN}C) from {ghg_choice} emissions between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice}<br>accounting framework with data from the {dataset_choice} datasets"

        #graph_title = f"(E)"
        #print(sorted_data)
        #print("Grandfathering (warming rights)")
        #print(len(sorted_data))

    else:   # This is Grandfathering (emissions rights)
        sorted_data = sorted_data
        y_axis_data = 'Value'
        graph_title = f"Countries' historical {ghg_choice} emissions (in kt) between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} dataset"
        #print("Grandfathering (emissions rights)")
        #print(len(sorted_data))

    sorted_df4 = sorted_data   
    #sorted_df4 = sorted_data.reset_index()

    # print(country_to_highlight)
    # print(country_highlight_options)
    # print(sorted_df4['Code'])
    # print(sorted_df4['Code'].to_list())
    # #index = sorted_df4['Code']
    # index = sorted_df4['Code'].to_list().index("QAT")
    # print(index)

    if ("warming" in principle_choice):
        index = sorted_df4['Code'].to_list().index(country_to_highlight)
        #index = sorted_df4.index[sorted_df4.Code==country_to_highlight].to_list()
        color_discrete_sequence = ['#ec7c34']*len(sorted_df4)
        #color_discrete_sequence[index[0]] = '#609cd4'
        color_discrete_sequence[index] = '#609cd4'
        #print(index)
    else:
        index = sorted_df4['Code'].to_list().index(country_to_highlight)
        #index = sorted_df4.index[sorted_df4.Code==country_to_highlight].to_list()
        color_discrete_sequence = ['#5A5A5A']*len(sorted_df4)
        #color_discrete_sequence[index[0]] = '#ec7c34'
        color_discrete_sequence[index] = '#ec7c34'
        #print(index)

    if (country_all_choice != 'All countries'):
        country_amount_choice = number_of_countries.get(country_amount)
        if "Top" in country_amount:  
            sorted_df4 = sorted_df4.head(country_amount_choice)
        else:
            sorted_df4 = sorted_df4.tail(country_amount_choice)

    fig = px.bar(sorted_df4,
                 x='Code',
                 y=y_axis_data,
                 #labels=["Country","Cost $US billions"],
                 title= graph_title,
                 labels=dict(x="Contribution US$"),
                 color=sorted_df4['Code'],
                 color_discrete_sequence = color_discrete_sequence
                 )
    
    # string = f"output1_{time_interval_selector_rights[0]}{time_interval_selector_rights[1]}{ghg_choice}.xlsx"
    
    # sorted_df4.to_excel(string)
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(plot_bgcolor = "white")
    if ("capita" in principle_choice):
        fig.update_layout(xaxis_title="Country code", yaxis_title="Historical (per capita) use")
    else:
        fig.update_layout(xaxis_title="Country code", yaxis_title="Historical use")

    # data_for_table = sorted_df4
    # # Change "Value" below to "New"
    
    # data_for_table['Value'] = sorted_df4[y_axis_data]
    # data_for_table['Value'] = data_for_table['Value'].map('{:,.3f}'.format)
    # data_for_table['Rank'] = range(1, len(data_for_table)+ 1)
    # #print(data_for_table)

    # data_for_table = data_for_table[['Rank', 'Country', 'Code', 'Value']]
    # # data_for_table = data_for_table.rename(columns={'Code':'Country Code'}, inplace=True)
    # # data_for_table = data_for_table.rename(columns={'Value':'Cost (US$)'}, inplace=True)
    # #data_for_table = data_for_table[0:9]

    # #return fig, data_for_table[0:10].to_dict('records')
    # return fig, data_for_table.to_dict('records')
    
    return fig


## Activate the following callback update ###
@callback(
    Output('rights-to-future-budget-graph', 'figure'),
    #Output('table-rights','data'),
    [Input('principle-dropdown2', 'value'),
    Input('dataset-dropdown-rights', 'value'),
    Input('accounting-dropdown-rights','value'),
    Input('sector-radio-all-or-single-rights','value'),
    Input('sector-dropdown-rights','value'),
    Input('ghg-dropdown-rights','value'),
    Input('metric-dropdown-rights', 'value'),
    Input ('time-interval-selector1-rights', 'value'),
    Input ('time-interval-selector2-rights', 'value'),
    Input ('time-interval-selector3-rights', 'value'),
    Input ('country-radio-all-or-top-rights', 'value'),
    Input ('country-amount', 'value'),
    Input('pop-growth-scenario-dropdown-rights', 'value'),
    Input('time-interval-selector-rights-future', 'value'),
    #Input('country-to-highlight','value'),
    ])

def rights_to_future_budget_graph(principle_choice, dataset_choice, accounting_choice, sector_all_choice, sector_single_choice, ghg_choice, metric_choice, time_interval_selector1_rights, time_interval_selector2_rights, time_interval_selector3_rights, country_all_choice, country_amount, pop_growth_scenario, time_interval_selector_pop): #country_to_highlight):

    if (dataset_choice == 'Eora-26'):
        time_interval_selector_rights = time_interval_selector1_rights
    elif (dataset_choice == 'UNFCCC'):
        time_interval_selector_rights = time_interval_selector2_rights
    else:
        time_interval_selector_rights = time_interval_selector3_rights

    year_range = list(range(time_interval_selector_rights[0], time_interval_selector_rights[1]+1))

    # Here we are checking whether all sectors have been selected or not, include all countries
    if (sector_all_choice == 'All sectors'):
        data = df.loc[(df.Dataset.apply(lambda x: x == dataset_choice)) & (df.Accounting.apply(lambda x: x == accounting_choice)) & (df.Gas.apply(lambda x: x == ghg_choice)) & (df.Metric.apply(lambda x: x == metric_choice)) & (df.Year.isin(year_range))]
        data2 = data.reset_index()
    else:
        data = df.loc[(df.Dataset.apply(lambda x: x == dataset_choice)) & (df.Accounting.apply(lambda x: x == accounting_choice)) & (df.Sector.apply(lambda x: x == sector_single_choice)) & (df.Gas.apply(lambda x: x == ghg_choice)) & (df.Metric.apply(lambda x: x == metric_choice)) & (df.Year.isin(year_range))]
        data2 = data.reset_index()

    ################################################################################################
        
    finance_choice = float(100)

    start_year_choice = time_interval_selector_rights[0]
    end_year_choice = time_interval_selector_rights[1]

    ey_data = data2.loc[(data2.Year.apply(lambda x: x == int(end_year_choice)))]
    sy_data = data2.loc[(data2.Year.apply(lambda x: x == int(start_year_choice)))]

    ey_data = ey_data.reset_index()
    ey_data = ey_data.fillna(0)
    sy_data = sy_data.reset_index()
    sy_data = sy_data.fillna(0)

    # Getting historical population numbers
    historical_populations = df_historical_pop_estimates.loc[(df_historical_pop_estimates.Year.isin(year_range))]
    historical_populations = historical_populations.reset_index()
    historical_person_years = historical_populations.groupby(['Country','Code'])['Historical_population_estimate'].sum().reset_index()
    historical_person_years = historical_person_years.rename(columns={'Historical_population_estimate':'Historical_person_years'})

    # First step: calculate warming amounts, for those principles that need it
    if ("warming" in principle_choice):
    # Calculations below this point relate to applying warming amounts
        
        ey_data['Temp_difference'] = (ey_data['G_anthro'] - ey_data['Value']) - (sy_data['G_anthro'] - sy_data['Value'])
        ey_data['Finance_share'] = (ey_data['Temp_difference']/sum(ey_data['Temp_difference']))*finance_choice
        # If you wanted to look at warming from nitrous oxide as a proportion of total warming then you would need to have
        # a different line to the one directly above which would divide by the G_anthro difference between the start and end years.
        #ey_data['Finance_share'] = ey_data['Temp_difference']

        sorted_data = ey_data.sort_values('Temp_difference', ascending=False)
        # IT MIGHT MAKE SENSE TO SWITCH FROM FINANCE SHARE TO TEMP DIFFERENCE
        #sorted_data = ey_data.sort_values('Temp_difference', ascending=False)

        #y_axis_data = 'Temp_difference'
        #graph_title = f"Countries' historical shares of warming (in \N{DEGREE SIGN}C) from {ghg_choice} emissions between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} datasets"
        
    else:
        # Just add the greenhouse gas values together for now
        # ey_data = ey_data.groupby('Code')['Value'].sum()
        # sy_data = sy_data.groupby('Code')['Value'].sum()
        # print(sy_data)
        
        data2 = data2.groupby(['Country','Code'])['Value'].sum().reset_index()
        data2['Finance_share'] = (data2['Value']/sum(data2['Value']))*finance_choice
        #sorted_data = data2.sort_values('Temp_difference', ascending=False)
        sorted_data = data2.sort_values('Value', ascending=False)
        
        #y_axis_data = 'Value'
        #graph_title = f"Countries' historical shares of {ghg_choice} emissions (in kt) between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} dataset"

    # Second step: calculate per capita amounts, for those principles that need it
    if ("HCPCCW" in principle_choice): # This is HCPCCW
        # ####### Second step is to join the warming/emissions datasets with the cumulative capita dataset, based on the country codes
        # This means then that the 'sorted data' and 'y' input values in the code to make the graph below should be different.
        data_with_person_years = sorted_data.merge(historical_person_years[['Code','Historical_person_years']],left_on='Code', right_on='Code')
        #### Check if a per capita principle has been selected. If one has, then calculate the number of cumulative person years
        data_with_person_years['Historical_per_capita'] = data_with_person_years['Temp_difference']/data_with_person_years['Historical_person_years']
        data_with_person_years = data_with_person_years.sort_values('Historical_per_capita', ascending=False)
        sorted_data = data_with_person_years
        y_axis_data = 'Historical_per_capita'
        graph_title = f"Countries' cumulative historical per cumulative capita warming (in \N{DEGREE SIGN}C) from {ghg_choice} emissions between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} datasets"
        
        #graph_title = f"(B)"
        # print("HPCCW")
        # print(len(sorted_data))
    
    elif ("HCPCCE" in principle_choice): # This is HCPCCE
        data_with_person_years = sorted_data.merge(historical_person_years[['Code','Historical_person_years']],left_on='Code', right_on='Code')
        #### Check if a per capita principle has been selected. If one has, then calculate the number of cumulative person years
        data_with_person_years['Historical_per_capita'] = data_with_person_years['Value']/data_with_person_years['Historical_person_years']
        data_with_person_years = data_with_person_years.sort_values('Historical_per_capita', ascending=False)
        sorted_data = data_with_person_years
        y_axis_data = 'Historical_per_capita'
        graph_title = f"Countries' cumulative historical per cumulative capita {ghg_choice} emissions (in kt) between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} dataset"
        # print("HPCCE")
        # print(len(sorted_data))
    
    elif ("ECPCCW" in principle_choice): # This is ECPCCW

        ##### This is old code beneath this point

        # # ####### Second step is to join the warming/emissions datasets with the cumulative capita dataset, based on the country codes
        # # This means then that the 'sorted data' and 'y' input values in the code to make the graph below should be different.
        # data_with_person_years = sorted_data.merge(historical_person_years[['Code','Historical_person_years']],left_on='Code', right_on='Code')
        # #### Check if a per capita principle has been selected. If one has, then calculate the number of cumulative person years
        # data_with_person_years['Historical_per_capita'] = data_with_person_years['Temp_difference']/data_with_person_years['Historical_person_years']
        # data_with_person_years = data_with_person_years.sort_values('Historical_per_capita', ascending=False)
        # sorted_data = data_with_person_years
        
        # y_axis_data = 'Historical_per_capita'
        # graph_title = f"Countries' historical per capita warming (in \N{DEGREE SIGN}C) from {ghg_choice} emissions between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} datasets"
        # #print("HPCCW")
        # #print(len(sorted_data))

        ##### This is old code above this point

        ######## THIS IS WHERE YOU WANT TO ADD THE CALCULATIONS FOR FUTURE PER CAPITA RIGHTS. BE CAREFUL WITH SMALL NUMBERS HERE
        # 0. Get year range for future population.
        year_range_for_future_population = list(range(time_interval_selector_pop[0], time_interval_selector_pop[1]+1))
        
        # 1. Get future population datasets
        future_populations = df_future_pop_scenarios.loc[(df_future_pop_scenarios.Pop_scenario.apply(lambda x: x == pop_growth_scenario)) & (df_future_pop_scenarios.Year.isin(year_range_for_future_population))]
        future_populations.reset_index()
        future_person_years = future_populations.groupby(['Country','Code'])['Population'].sum().reset_index()
        future_person_years = future_person_years.rename(columns={'Population':'Future_person_years'})

        # 2. Merge historical population and future population datasets
        df_with_future_person_years = historical_person_years.merge(future_person_years[['Code','Future_person_years']],left_on='Code', right_on='Code') #.drop('Code',axis='columns')
        #print('df with future person years')
        #print(df_with_future_person_years)
        # 2.5 Merge warming information with population datasets (historical and future)
        df_with_all_info = sorted_data.merge(df_with_future_person_years[['Code', 'Historical_person_years','Future_person_years']],left_on='Code', right_on='Code')
        #print('df with all info')
        #print(df_with_all_info)

        # 3. Calculate the total person years
        df_with_all_info['Total_person_years'] = df_with_all_info['Historical_person_years'] + df_with_all_info['Future_person_years']

        # 4. Calculate:
        # - historical warming
        world_historical_warming = df_with_all_info['Temp_difference'].sum() #<- This is generating the current Temp_difference error
        # - world warming limit
        world_warming_limit = 2*world_historical_warming
        # - world historical person years
        world_historical_person_years = df_with_all_info['Historical_person_years'].sum()
        # - world future person years
        world_future_person_years = df_with_all_info['Future_person_years'].sum()
        # - world total person years
        world_total_person_years = df_with_all_info['Total_person_years'].sum()
        # - world equal cumulative capita amount of warming
        world_equal_cumulative_capita_amount_warming = world_warming_limit/world_total_person_years
        # - cumulative capita warming
        cumulative_capita_warming = world_historical_warming/world_total_person_years

        df_with_all_info['EPC_fair_share'] = df_with_all_info['Total_person_years']*world_equal_cumulative_capita_amount_warming
        df_with_all_info['EPC_budget'] = df_with_all_info['EPC_fair_share'].sub(df_with_all_info['Temp_difference'])

        sorted_data = df_with_all_info.sort_values('EPC_budget', ascending=False)
        y_axis_data = 'EPC_budget'
        graph_title = f"Countries' equal per capita shares of warming (in \N{DEGREE SIGN}C) based upon historical {ghg_choice} emissions between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, under the {accounting_choice}<br>accounting framework with data from the {dataset_choice} datasets"

        #graph_title = f"(B)"

    elif ("ECPCCE" in principle_choice): # This is ECPCCE
        
        ##### This is old code beneath this point

        # data_with_person_years = sorted_data.merge(historical_person_years[['Code','Historical_person_years']],left_on='Code', right_on='Code')
        # #### Check if a per capita principle has been selected. If one has, then calculate the number of cumulative person years
        # data_with_person_years['Historical_per_capita'] = data_with_person_years['Value']/data_with_person_years['Historical_person_years']
        # data_with_person_years = data_with_person_years.sort_values('Historical_per_capita', ascending=False)
        # sorted_data = data_with_person_years
        # y_axis_data = 'Historical_per_capita'
        # graph_title = f"Countries' historical per capita {ghg_choice} emissions (in kt) between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice}<br>accounting framework with data from the {dataset_choice} dataset"
        # #print("HPCCE")
        # #print(len(sorted_data))

        ##### This is old code above this point

        ######## THIS IS WHERE YOU WANT TO ADD THE CALCULATIONS FOR FUTURE PER CAPITA RIGHTS. BE CAREFUL WITH SMALL NUMBERS HERE
        # 0. Get year range for future population.
        year_range_for_future_population = list(range(time_interval_selector_pop[0], time_interval_selector_pop[1]+1))
        
        # 1. Get future population datasets
        future_populations = df_future_pop_scenarios.loc[(df_future_pop_scenarios.Pop_scenario.apply(lambda x: x == pop_growth_scenario)) & (df_future_pop_scenarios.Year.isin(year_range_for_future_population))]
        future_populations.reset_index()
        future_person_years = future_populations.groupby(['Country','Code'])['Population'].sum().reset_index()
        future_person_years = future_person_years.rename(columns={'Population':'Future_person_years'})

        # 2. Merge historical population and future population datasets
        df_with_future_person_years = historical_person_years.merge(future_person_years[['Code','Future_person_years']],left_on='Code', right_on='Code') #.drop('Code',axis='columns')
        #print('df with future person years')
        #print(df_with_future_person_years)
        # 2.5 Merge warming information with population datasets (historical and future)
        df_with_all_info = sorted_data.merge(df_with_future_person_years[['Code', 'Historical_person_years','Future_person_years']],left_on='Code', right_on='Code')
        #print('df with all info')
        #print(df_with_all_info)

        # 3. Calculate the total person years
        df_with_all_info['Total_person_years'] = df_with_all_info['Historical_person_years'] + df_with_all_info['Future_person_years']

        # 4. Calculate:
        # - historical warming
        world_historical_warming = df_with_all_info['Value'].sum() #<- This (when it used to be Temp_difference instead of Value) was generating the current Temp_difference error
        # - world warming limit
        world_warming_limit = 2*world_historical_warming
        # - world historical person years
        world_historical_person_years = df_with_all_info['Historical_person_years'].sum()
        # - world future person years
        world_future_person_years = df_with_all_info['Future_person_years'].sum()
        # - world total person years
        world_total_person_years = df_with_all_info['Total_person_years'].sum()
        # - world equal cumulative capita amount of warming
        world_equal_cumulative_capita_amount_warming = world_warming_limit/world_total_person_years
        # - cumulative capita warming
        cumulative_capita_warming = world_historical_warming/world_total_person_years

        df_with_all_info['EPC_fair_share'] = df_with_all_info['Total_person_years']*world_equal_cumulative_capita_amount_warming
        df_with_all_info['EPC_budget'] = df_with_all_info['EPC_fair_share'].sub(df_with_all_info['Value'])

        sorted_data = df_with_all_info.sort_values('EPC_budget', ascending=False)

        y_axis_data = 'EPC_budget'
        graph_title = f"Countries' equal per capita shares of {ghg_choice} emissions based upon historical {ghg_choice} emissions (in kt) between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, under the {accounting_choice}<br>accounting framework with data from the {dataset_choice} dataset"

    elif (("Grandfathering" in principle_choice) & ("warming" in principle_choice)): # This is Grandfathering (warming rights)
        sorted_data = sorted_data
        y_axis_data = 'Temp_difference'
        graph_title = f"Countries' historical warming (in \N{DEGREE SIGN}C) from {ghg_choice} emissions between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice}<br>accounting framework with data from the {dataset_choice} datasets"
        #print(sorted_data)
        #print("Grandfathering (warming rights)")
        #print(len(sorted_data))
        #graph_title = f"(F)"

    else:   # This is Grandfathering (emissions rights)
        sorted_data = sorted_data
        y_axis_data = 'Value'
        graph_title = f"Countries' historical {ghg_choice} emissions (in kt) between {time_interval_selector_rights[0]} and {time_interval_selector_rights[1]}, based on the {accounting_choice} accounting framework<br>with data from the {dataset_choice} dataset"
        #print("Grandfathering (emissions rights)")
        #print(len(sorted_data))

    sorted_df4 = sorted_data   
    #sorted_df4 = sorted_data.reset_index()

    if ("warming" in principle_choice):
        #index = sorted_df4.index[sorted_df4.Code==country_to_highlight].to_list()
        color_discrete_sequence = ['#ec7c34']*len(sorted_df4)
        #color_discrete_sequence[index[0]] = '#609cd4'
    else:
        #index = sorted_df4.index[sorted_df4.Code==country_to_highlight].to_list()
        color_discrete_sequence = ['#5A5A5A']*len(sorted_df4)
        #color_discrete_sequence[index[0]] = '#ec7c34'

    if (country_all_choice != 'All countries'):
        country_amount_choice = number_of_countries.get(country_amount)
        if "Top" in country_amount:  
            sorted_df4 = sorted_df4.head(country_amount_choice)
        else:
            sorted_df4 = sorted_df4.tail(country_amount_choice)

    fig = px.bar(sorted_df4,
                 x='Code',
                 y=y_axis_data,
                 #labels=["Country","Cost $US billions"],
                 title= graph_title,
                 labels=dict(x="Contribution US$"),
                 color=sorted_df4['Code'],
                 color_discrete_sequence = color_discrete_sequence
                 )
    
    #sorted_df4.to_excel('output1.xlsx')
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(plot_bgcolor = "white")
    if ("capita" in principle_choice):
        fig.update_layout(xaxis_title="Country code", yaxis_title="Future shares")
    else:
        fig.update_layout(xaxis_title="Country code", yaxis_title="Future shares")

    # data_for_table = sorted_df4
    # # Change "Value" below to "New"
    
    # data_for_table['Value'] = sorted_df4[y_axis_data]
    # data_for_table['Value'] = data_for_table['Value'].map('{:,.3f}'.format)
    # data_for_table['Rank'] = range(1, len(data_for_table)+ 1)
    # #print(data_for_table)

    # data_for_table = data_for_table[['Rank', 'Country', 'Code', 'Value']]
    # # data_for_table = data_for_table.rename(columns={'Code':'Country Code'}, inplace=True)
    # # data_for_table = data_for_table.rename(columns={'Value':'Cost (US$)'}, inplace=True)
    # #data_for_table = data_for_table[0:9]

    # #return fig, data_for_table[0:10].to_dict('records')
    # return fig, data_for_table.to_dict('records')
    
    return fig


# #### Commenting out graph from this point onwards

# @callback(
#     Output('rights-to-future-budget-graph', 'figure'),
#     Output('table-rights','data'),
#     [Input('principle-dropdown', 'value'),
#     Input('dataset-dropdown-rights', 'value'),
#     Input('accounting-dropdown-rights','value'),
#     Input('sector-radio-all-or-single-rights','value'),
#     Input('sector-dropdown-rights','value'),
#     Input('ghg-dropdown-rights','value'),
#     Input('metric-dropdown-rights', 'value'),
#     Input ('time-interval-selector1-rights', 'value'),
#     Input ('time-interval-selector2-rights', 'value'),
#     Input ('time-interval-selector3-rights', 'value'),
#     Input ('country-radio-all-or-top-rights', 'value'),
#     Input ('country-amount', 'value'),
#     Input('pop-growth-scenario-dropdown-rights', 'value'),
#     Input('time-interval-selector-rights-future', 'value')
#     ])

#def rights_to_future_budget_graph(principle_choice, dataset_choice, accounting_choice, sector_all_choice, sector_single_choice, ghg_choice, metric_choice, time_interval_selector1_rights, time_interval_selector2_rights, time_interval_selector3_rights, country_all_choice, country_amount, pop_growth_scenario, time_interval_selector_pop):

#     if (dataset_choice == 'Eora-26'):
#         time_interval_selector_rights = time_interval_selector1_rights
#     elif (dataset_choice == 'UNFCCC'):
#         time_interval_selector_rights = time_interval_selector2_rights
#     else:
#         time_interval_selector_rights = time_interval_selector3_rights

#     year_range = list(range(time_interval_selector_rights[0], time_interval_selector_rights[1]+1))

#     # Here we are checking whether all sectors have been selected or not, include all countries
#     if (sector_all_choice == 'All sectors'):
#         data = df.loc[(df.Dataset.apply(lambda x: x == dataset_choice)) & (df.Accounting.apply(lambda x: x == accounting_choice)) & (df.Gas.apply(lambda x: x == ghg_choice)) & (df.Metric.apply(lambda x: x == metric_choice)) & (df.Year.isin(year_range))]
#         data2 = data.reset_index()
#     else:
#         data = df.loc[(df.Dataset.apply(lambda x: x == dataset_choice)) & (df.Accounting.apply(lambda x: x == accounting_choice)) & (df.Sector.apply(lambda x: x == sector_single_choice)) & (df.Gas.apply(lambda x: x == ghg_choice)) & (df.Metric.apply(lambda x: x == metric_choice)) & (df.Year.isin(year_range))]
#         data2 = data.reset_index()

#     ################################################################################################
        
#     finance_choice = float(100)

#     start_year_choice = time_interval_selector_rights[0]
#     end_year_choice = time_interval_selector_rights[1]

#     ey_data = data2.loc[(data2.Year.apply(lambda x: x == int(end_year_choice)))]
#     sy_data = data2.loc[(data2.Year.apply(lambda x: x == int(start_year_choice)))]

#     ey_data = ey_data.reset_index()
#     ey_data = ey_data.fillna(0)
#     sy_data = sy_data.reset_index()
#     sy_data = sy_data.fillna(0)

#     # Calculations below this point relate to applying warming amounts
#     if ((dataset_choice == 'CEDS, Houghton & Nassikas (2017) - All GHGs') | (dataset_choice == 'CEDS, Houghton & Nassikas (2017)')):

#         ey_data['Temp_difference'] = (ey_data['G_anthro'] - ey_data['Value']) - (sy_data['G_anthro'] - sy_data['Value'])
#         ey_data['Finance_share'] = (ey_data['Temp_difference']/sum(ey_data['Temp_difference']))*finance_choice
#         # If you wanted to look at warming from nitrous oxide as a proportion of total warming then you would need to have
#         # a different line to the one directly above which would divide by the G_anthro difference between the start and end years.
#         #ey_data['Finance_share'] = ey_data['Temp_difference']

#         sorted_data = ey_data.sort_values('Finance_share', ascending=False)
#         # IT MIGHT MAKE SENSE TO SWITCH FROM FINANCE SHARE TO TEMP DIFFERENCE
#         #sorted_data = ey_data.sort_values('Temp_difference', ascending=False)

#         graph_title = f"Countries' fair shares of future warming (in \N{DEGREE SIGN}C) from {ghg_choice}, according to the {principle_choice} Principle"

#     else:

#         # Just add the greenhouse gas values together for now
#         # ey_data = ey_data.groupby('Code')['Value'].sum()
#         # sy_data = sy_data.groupby('Code')['Value'].sum()
#         # print(sy_data)
#         data2 = data2.groupby(['Country','Code'])['Value'].sum().reset_index()
#         data2['Finance_share'] = (data2['Value']/sum(data2['Value']))*finance_choice
#         sorted_data = data2.sort_values('Finance_share', ascending=False)

#         graph_title = f"Countries' fair shares of {ghg_choice} emissions (in kt), according to the {principle_choice} Principle"

#     ####### In here is where you can start working on the population stuff
    
#     year_range_for_future_population = list(range(time_interval_selector_pop[0], time_interval_selector_pop[1]+1))
#     #print(year_range_for_future_population)

#     ####### First step is to group by country code and sum each country code's population over the time interval that has been selected.
#     ####### Country's historical person years
#     #print(sorted_data)
#     historical_populations = df_historical_pop_estimates.loc[(df_historical_pop_estimates.Year.isin(year_range))]
#     historical_populations = historical_populations.reset_index()
#     historical_person_years = historical_populations.groupby(['Country','Code'])['Historical_population_estimate'].sum().reset_index()

#     ### Commentented out from this point onwards

#     historical_person_years = historical_person_years.rename(columns={'Historical_population_estimate':'Historical_person_years'})
#     #print(historical_person_years)

#     # ####### Second step is to join the warming/emissions datasets with the cumulative capita dataset, based on the country codes
#     # This means then that the 'sorted data' and 'y' input values in the code to make the graph below should be different.
#     df3 = sorted_data.merge(historical_person_years[['Code','Historical_person_years']],left_on='Code', right_on='Code') #.drop('Code',axis='columns')
#     #print(df3)
#     #print(type(df3))

#     # ####### Third step is to do the calculation for the 163 countries, whereby these countries' emissions/warming is divided by their cumulative capita
#     # ####### Historical cumulative person years
#     if (principle_choice == "Equal cumulative per cumulative capita warming (ECPCCW)"):
#         df3['Historical_cumulative_per_capita'] = df3['Temp_difference']/df3['Historical_person_years']

#         # # Here is the population growth scenario information
#         future_populations = df_future_pop_scenarios.loc[(df_future_pop_scenarios.Pop_scenario.apply(lambda x: x == pop_growth_scenario)) & (df_future_pop_scenarios.Year.isin(year_range_for_future_population))]
#         future_populations.reset_index()
#         future_person_years = future_populations.groupby(['Country','Code'])['Population'].sum().reset_index()
#         future_person_years = future_person_years.rename(columns={'Population':'Future_person_years'})

#         df4 = df3.merge(future_person_years[['Code','Future_person_years']],left_on='Code', right_on='Code') #.drop('Code',axis='columns')

#         df4['Total_person_years'] = df4['Historical_person_years'] + df4['Future_person_years']
        
#         # Now you need to create the cumulative person years
#         # Now you need to create the cumulative fair budget per country.
#         # You want to only include the populations of those countries that are in the historical emissions/warming dataset.
#         # Here is where you can take future population growth scenarios into account
#         # Will need to distinguish between the different datasets, as some will have emissions and others will have warming.
#         world_historical_warming = df4['Temp_difference'].sum() #<- This is generating the current Temp_difference error
#         world_warming_limit = 1.1*world_historical_warming
#         world_historical_person_years = df4['Historical_person_years'].sum()
#         world_future_person_years = df4['Future_person_years'].sum()
#         world_total_person_years = df4['Total_person_years'].sum()
#         world_equal_cumulative_capita_amount_warming = world_warming_limit/world_total_person_years
#         cumulative_capita_warming = world_historical_warming/world_total_person_years

#         df4['EPC_fair_share'] = df4['Total_person_years']*world_equal_cumulative_capita_amount_warming
#         df4['EPC_budget'] = df4['EPC_fair_share'].sub(df4['Temp_difference'])
#         #print(df4.columns.values.tolist())
#         #print(df4)
#         # The column names are Country, Value, Finance_share, Historical_person_years and Historical_cumulative_per_capita
        
#         ####### Sort values and specify colours etc.
#         #sorted_df4 = df4.sort_values('Historical_cumulative_per_capita', ascending=False)
#         sorted_df4 = df4.sort_values('EPC_budget', ascending=False)
#         color_discrete_sequence = ['#609cd4']*len(sorted_df4)
#         y_axis_data = 'EPC_budget'

#     elif(principle_choice == "Equal cumulative per cumulative capita emissions (ECPCCE)"):
#         df3['Historical_cumulative_per_capita'] = df3['Value']/df3['Historical_person_years']

#         print("yes you are here!")

#         # # Here is the population growth scenario information
#         future_populations = df_future_pop_scenarios.loc[(df_future_pop_scenarios.Pop_scenario.apply(lambda x: x == pop_growth_scenario)) & (df_future_pop_scenarios.Year.isin(year_range_for_future_population))]
#         future_populations.reset_index()
#         future_person_years = future_populations.groupby(['Country','Code'])['Population'].sum().reset_index()
#         future_person_years = future_person_years.rename(columns={'Population':'Future_person_years'})

#         df4 = df3.merge(future_person_years[['Code','Future_person_years']],left_on='Code', right_on='Code') #.drop('Code',axis='columns')

#         df4['Total_person_years'] = df4['Historical_person_years'] + df4['Future_person_years']
        
#         # Now you need to create the cumulative person years
#         # Now you need to create the cumulative fair budget per country.
#         # You want to only include the populations of those countries that are in the historical emissions/warming dataset.
#         # Here is where you can take future population growth scenarios into account
#         # Will need to distinguish between the different datasets, as some will have emissions and others will have warming.
#         world_historical_emissions = df4['Value'].sum() #<- This is generating the current Temp_difference error
#         world_emissions_limit = 1.1*world_historical_emissions
#         world_historical_person_years = df4['Historical_person_years'].sum()
#         world_future_person_years = df4['Future_person_years'].sum()
#         world_total_person_years = df4['Total_person_years'].sum()
#         world_equal_cumulative_capita_amount_emissions = world_emissions_limit/world_total_person_years
#         print('world emissions limit')
#         print(world_emissions_limit)
#         print(type(world_emissions_limit))
#         print('world total person years')
#         print(world_total_person_years)
#         print(type(world_total_person_years))

#         cumulative_capita_emissions = world_historical_emissions/world_total_person_years

#         print('world_historical_emissions')
#         print(world_historical_emissions)
#         print(type(world_historical_emissions))
#         print('world_total_person_years')
#         print(world_total_person_years)
#         print(type(world_total_person_years))


#         print(world_equal_cumulative_capita_amount_emissions)

#         df4['EPC_fair_share'] = df4['Total_person_years']*world_equal_cumulative_capita_amount_emissions
#         df4['EPC_budget'] = df4['EPC_fair_share'].sub(df4['Value'])
#         #print(df4.columns.values.tolist())
#         #print(df4)
#         # The column names are Country, Value, Finance_share, Historical_person_years and Historical_cumulative_per_capita
        
#         ####### Sort values and specify colours etc.
#         #sorted_df4 = df4.sort_values('Historical_cumulative_per_capita', ascending=False)
#         sorted_df4 = df4.sort_values('EPC_budget', ascending=False)
#         color_discrete_sequence = ['#609cd4']*len(sorted_df4)
#         y_axis_data = 'EPC_budget'

#     elif(principle_choice == "Grandfathering (warming rights)"):
        
#         # Copy the code from above
#         print('You are in grandfathering (warming rights)')
        
#         sorted_df4 = sorted_data
#         #sorted_df4 = sorted_data.sort_values('Finance_share', ascending=False)
#         color_discrete_sequence = ['#609cd4']*len(sorted_df4)
#         y_axis_data = 'Temp_difference'
#     else: #This is the option where (principle_choice == "Grandfathering (emissions rights)")

#         # Copy the code from above
#         print('You are in grandfathering (emissions rights)')

#         sorted_df4 = sorted_data
#         #sorted_df4 = sorted_data.sort_values('Finance_share', ascending=False)
#         color_discrete_sequence = ['#609cd4']*len(sorted_df4)
#         y_axis_data =  'Value'

#     if (country_all_choice != 'All countries'):
#         country_amount_choice = number_of_countries.get(country_amount)
#         if "Top" in country_amount:  
#             sorted_df4 = sorted_df4.head(country_amount_choice)
#         else:
#             sorted_df4 = sorted_df4.tail(country_amount_choice)

#     # if "warming" in principle_choice:
#     #     y_axis_data = 'ECP_budget'
#     # else:
#     #     y_axis_data =  'Value'

#     fig = px.bar(sorted_df4,
#                 x='Code',
#                 y=y_axis_data,
#                 #labels=["Country","Cost $US billions"],
#                 title= graph_title,
#                 labels=dict(x="Contribution US$"),
#                 color=sorted_df4['Code'],
#                 color_discrete_sequence = color_discrete_sequence
#                 )
    
#     #print(sum(sorted_df4['Temp_difference']))               
#     #sorted_df4.to_excel('output1.xlsx')
    
#     fig.update_xaxes(showgrid=False)
#     fig.update_yaxes(showgrid=False)
#     fig.update_layout(plot_bgcolor = "white")
#     fig.update_layout(xaxis_title="Country code", yaxis_title="Fair share")

#     data_for_table = sorted_df4
#     # Change "Value" below to "New"
    
#     data_for_table['Value'] = sorted_df4[y_axis_data]
#     data_for_table['Value'] = data_for_table['Value'].map('{:,.3f}'.format)
#     data_for_table['Rank'] = range(1, len(data_for_table)+ 1)
#     #print(data_for_table)

#     data_for_table = data_for_table[['Rank', 'Country', 'Code', 'Value']]
#     # data_for_table = data_for_table.rename(columns={'Code':'Country Code'}, inplace=True)
#     # data_for_table = data_for_table.rename(columns={'Value':'Cost (US$)'}, inplace=True)
#     #data_for_table = data_for_table[0:9]

#     #return fig, data_for_table[0:10].to_dict('records')
#     return fig, data_for_table.to_dict('records')
    
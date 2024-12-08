import dash
from dash import dcc, html, dash_table, callback, Input, Output
import pandas as pd
import plotly.express as px
import os
# import numpy as np
# print(np.__version__)

dash.register_page(__name__)

thisPath = os.path.abspath(os.path.dirname(__file__))

df_temps = pd.read_csv(os.path.join(thisPath, os.pardir,'warmingCallahan&Mankin_ind_GHGs.csv'), index_col=None, encoding='cp1252', low_memory=False)
df_temps_all = pd.read_csv(os.path.join(thisPath, os.pardir,'warmingCallahan&Mankin_ALL_GHGs.csv'), index_col=None, encoding='cp1252', low_memory=False)

countriesDictionary = {
    "Top 10": 10,
    "Top 50": 50,
    "Top 100": 100
}

ghgDictionary = {
    "CO2": "CO2",
    "CH4": "CH4",
    "NOx": "NOx"
}

startDateDictionary = {
    "1850": 1850,
    "1960": 1960,
    "1990": 1990
}

endDateDictionary = {
    "1960": 1960,
    "1990": 1990,
    "2014": 2014
}

number_of_countries = {
    "Top 10": 10,
    "Top 20": 20,
    "Top 50": 50,
    "Top 100": 100
}



accounting_frameworks = ['Production-based','Consumption-based']

total_country_options = df_temps['Code'].unique()

subset_countries_options = df_temps_all['Country'].unique()
radio_country_options = ['All countries', 'Some other number of countries']
radio_ghg_options = ['All three main GHGs', 'One or two of the main GHGs']

columns_reordered = df_temps_all[["Rank","Country", "Code", "Temp_difference"]]

layout = html.Div([ 

    html.Div(
        children=[
            html.Div(
                className="user-selections-party-p1",#id='grid-container',
                children=[
                    html.Div([
                        html.H1('RQ1: What are countries\' contributions to warming?'),

                        html.H4('Country'), #className="selector-def"),
                        dcc.Dropdown(id='country-dropdown-warming',
                                    options=[{'label': i, 'value': i} for i in total_country_options],
                                    value=total_country_options[19]), #73),

                        html.H4('Greenhouse gas options'),
                        dcc.RadioItems(id='ghg-radio-all-or-less',
                                options=[{'label': i, 'value': i} for i in radio_ghg_options],
                                value=radio_ghg_options[0],
                                inline=True),
                        
                        ### Put the following code inside a container, only to be displayed if the single country option is ticked in the checklist
                        html.Div(id='single-ghg-choices-container', children=[
                            dcc.Dropdown(id='ghg-dropdown',
                                        options = list(ghgDictionary),
                                        value = list(ghgDictionary),
                                        multi =True)
                        ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback

                        html.H4('Start year'),
                        dcc.Dropdown(
                            id='start-date-dropdown',
                            options=[{'label': i, 'value': i} for i in startDateDictionary.keys()],
                            value=list(startDateDictionary)[0],
                            multi=False
                            ),

                        html.H4('End year'),
                        dcc.Dropdown(
                            id='end-date-dropdown',
                            options=[{'label': i, 'value': i} for i in endDateDictionary.keys()],
                            value=list(endDateDictionary)[0],
                            multi=False
                        ),
                        html.H4('Choice of countries'),
                            dcc.RadioItems(id='country-radio-all-or-top',
                                    options=radio_country_options,
                                    value=radio_country_options[0]), 

                            ### Put the following code inside a container, only to be displayed if the top 50 country option is ticked in the checklist
                            html.Div(id='top-country-choices-container', children=[

                                dcc.Dropdown(
                                    id='country-amount',
                                    options=[{'label': i, 'value': i} for i in number_of_countries.keys()],
                                    value=list(number_of_countries)[0]),

                            ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback                   
                    ],id='left-container')     
                ]
            ),
            html.Div(id='graph-container', children=[
                html.Div([
                    dcc.Graph(
                    id='warming-graph',style={'padding': 10})
                ], id='right-container'),

            html.Div(id='table-container-warming', children=[
                html.Div([
                    dash_table.DataTable(
                        columns = [{"name": i, "id": i} for i in columns_reordered],
                        data=df_temps_all[0:10].to_dict('records'),
                        style_header={
                                      'backgroundColor': '#ec7c34', #'#e1e4eb',
                                      'fontWeight': 'bold',
                                      'align': 'center'},
                        style_cell={'fontSize':16, 'font-family':'Arial',
                                    'minWidth': '100px', 'width': '100px', 'maxWidth': '300px',
                                    'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'textAlign': 'left',},
                        id='table-warming'),
                        
                ], id='tab-container', style={'padding':10})
            ])
            ])
        ]
    )
])

######################### Start year and end year call backs #########################

@callback(
    Output('end-date-dropdown','options'),
    [Input('start-date-dropdown', 'value')
    ])
def set_end_date_from_start_date_dropdown(start_date_choice):
    if start_date_choice == "1850":
        end_date_choice = ["1960", "1990", "2014"]
    elif start_date_choice == "1960":
        end_date_choice = ["1990", "2014"]
    else:
        end_date_choice = ["2014"]
    return end_date_choice

#####################################################################################

# ######################### Single country choices containers #########################

@callback(
   Output('single-ghg-choices-container', 'style'),
   [Input('ghg-radio-all-or-less', 'value')
])
def show_hide_single_ghg_choices_container(visibility_state):
    if visibility_state == 'One or two of the main GHGs':
        return {'display': 'block'}
    return {'display': 'none'}

# #####################################################################################


######################## Top 50 countries choices containers #########################

@callback(
   Output('top-country-choices-container', 'style'),
   Input('country-radio-all-or-top', 'value')
   #Input('top-50','value')
)
def show_hide_top_country_choices_container(visibility_state):
    if visibility_state == 'Some other number of countries':
        return {'display': 'block'}
    return {'display': 'none'}

####################################################################################

@callback(
    Output('warming-graph', 'figure'),
    Output('table-warming','data'),
    [Input('country-dropdown-warming','value'),
    Input('ghg-radio-all-or-less', 'value'),
    Input('ghg-dropdown', 'value'),
    Input('start-date-dropdown','value'),
    Input('end-date-dropdown','value'),
    Input('country-radio-all-or-top', 'value'),
    Input ('country-amount', 'value'),
    ])

def warming_graph(country_choice, ghg_all_choice, ghg_choice, start_year_choice, end_year_choice, country_all_choice, country_amount):

    
    ####################### First dataframe - end year (ey)

    # Do a check here for if only one country has been selected
    # Here we are checking whether all sectors have been selected or not, for the selected country
    if (ghg_all_choice == 'All three main GHGs'):
        ey_data = df_temps_all.loc[(df_temps_all.Year.apply(lambda x: x == int(end_year_choice)))]
    else:
        ey_data = df_temps.loc[(df_temps.Year.apply(lambda x: x == int(end_year_choice))) & (df_temps.Gas.isin(ghg_choice))]
        #ey_data = ey_data.groupby('Code')['Temperature'].sum()
        ey_data = ey_data.groupby(['Code', 'Country'], as_index=False).sum()
        #ey_data = ey_data.groupby(['Code','Temperature']).sum().reset_index()
        #print("you should be seeing a Gas column")
        #print(ey_data)

    ey_data = ey_data.reset_index()
    ey_data = ey_data.fillna(0)

    ####################### Second dataframe - start year (sy)

    # Do a check here for if only one country has been selected
    # Here we are checking whether all sectors have been selected or not, for the selected country
    if (ghg_all_choice == 'All three main GHGs'):
        sy_data = df_temps_all.loc[(df_temps_all.Year.apply(lambda x: x == int(start_year_choice)))]
        #sy_data = sy_data
    else:
        sy_data = df_temps.loc[(df_temps.Year.apply(lambda x: x == int(start_year_choice))) & (df_temps.Gas.isin(ghg_choice))]
        #sy_data = sy_data.groupby('Code')['Temperature'].sum(),
        sy_data = sy_data.groupby(['Code', 'Country'], as_index=False).sum()
        #sy_data = sy_data.groupby(['Code','Country'['Temperature'].sum()
        #print("you should be seeing a Gas column")
        #print('temp df')
        #print(df_temps)
        #print(ghg_choice)
        #print(sy_data)

    sy_data = sy_data.reset_index()
    sy_data = sy_data.fillna(0)

    ####################### Now calculate the difference between the two dataframes to get the change in temperature and sort in ascending order

    # Below code is old code
    #sorted_data = data.sort_values('Difference',ascending=False) #[1:10]

    ey_data['Temp_difference'] = (ey_data['G_anthro'] - ey_data['Temperature']) - (sy_data['G_anthro'] - sy_data['Temperature'])
    
    
    sorted_data = ey_data.sort_values('Temp_difference', ascending=False)

    # New code here:
    #sorted_data = sorted_data.groupby(['Code','Country'])['Temp_difference'].sum()
    #sorted_data = sorted_data.sort_values('Temp_difference', ascending=False)

    sorted_data = sorted_data.reset_index()
    sorted_data = sorted_data.fillna(0)
    print('sorted data')
    print(sorted_data)

    if (country_all_choice != 'All countries'):
        country_amount_choice = number_of_countries.get(country_amount)
        sorted_data = sorted_data.head(country_amount_choice)
        #sorted_data = sorted_data.reset_index()
        #sorted_data = sorted_data.fillna(0)

    # Different titles for the graph
    if (ghg_all_choice == 'All three main GHGs'):
        graph_title = f"Countries' contributions to warming (\N{DEGREE SIGN}C) between {start_year_choice} and {end_year_choice} from the three main GHGs"
    #     if ((start_year_choice == '1850') & (end_year_choice == '1960')):
    #         graph_title = f"(A)"
    #     elif ((start_year_choice == '1850') & (end_year_choice == '1990')):
    #         graph_title = f"(B)"
    #     elif ((start_year_choice == '1850') & (end_year_choice == '2014')):
    #         graph_title = f"(C)"
    #     elif ((start_year_choice == '1960') & (end_year_choice == '1990')):
    #         graph_title = f"(D)"
    #     elif ((start_year_choice == '1960') & (end_year_choice == '2014')):
    #         graph_title = f"(E)"
    #     else:
    #         graph_title = f"(F)"

    else:
        graph_title = f"Countries' contributions to warming (\N{DEGREE SIGN}C) between {start_year_choice} and {end_year_choice} from {ghg_choice}"
    #     if ((start_year_choice == '1850') & (end_year_choice == '1960')):
    #         graph_title = f"(A)"
    #     elif ((start_year_choice == '1850') & (end_year_choice == '1990')):
    #         graph_title = f"(B)"
    #     elif ((start_year_choice == '1850') & (end_year_choice == '2014')):
    #        graph_title = f"(C)"
    #     elif ((start_year_choice == '1960') & (end_year_choice == '1990')):
    #        graph_title = f"(D)"
    #     elif ((start_year_choice == '1960') & (end_year_choice == '2014')):
    #        graph_title = f"(E)"
    #     else:
    #        graph_title = f"(F)"

    index = sorted_data.index[sorted_data.Code==country_choice].to_list()
    color_discrete_sequence = ['#ec7c34']*len(sorted_data)
    color_discrete_sequence[index[0]] = '#609cd4'

    fig = px.bar(sorted_data,
                 x='Code',
                 y='Temp_difference',
                 title=graph_title,
                 labels=dict(x="Contribution US$"),
                 color=sorted_data['Code'],
                 color_discrete_sequence = color_discrete_sequence
                 )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(plot_bgcolor = "white")
    fig.update_layout(xaxis_title="Country code", yaxis_title="Temperature contribution (\N{DEGREE SIGN}C)")

    data_for_table = sorted_data
    #data_for_table['Value'] = data_for_table['Value']/1000000000

    data_for_table['Temp_difference'] = data_for_table['Temp_difference'].map('{:,.3f}'.format)
    data_for_table['Rank'] = range(1, len(data_for_table)+ 1)
    print(data_for_table)

    data_for_table = data_for_table[['Rank', 'Country', 'Code', 'Temp_difference']]
    
    return fig, data_for_table[0:10].to_dict('records')
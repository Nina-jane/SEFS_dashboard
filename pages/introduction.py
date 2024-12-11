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
                            '''Welcome to the Science and Ethics of Fair Shares (SEFS) dashboard.''', html.Br(),html.Br(),'''
                            This dashboard is the output of a doctoral research project, which sought to answer the following overarching research question (RQ):''', html.Br(),html.Br(),''' 
                            Can applying ethical distributional principles within a dashboard shed light on nation-state effort-sharing for addressing climate change?''', html.Br(),html.Br(),'''
                            Pages 2-4 focus on answering the following three sub RQs:''', html.Br(),html.Br(),'''        
                            RQ1: What are countries\' historical contributions to global warming?''', html.Br(),'''   
                            RQ2: How should the costs of climate change be distributed between countries?''', html.Br(),'''   
                            RQ3: How should rights to emit and warming rights be distributed between countries?''', html.Br(),html.Br(),html.Br(),'''      

                            The dashboard has been developed with the communities of international climate change negotiators and policymakers in mind. These communities will continue grappling with these questions and possible effort-sharing approaches for addressing climate change equitably at the international level.'''], style={'textAlign': 'left'}
                            ),
                        # html.Button("Update"),
                        ], id='left-container'),
                        # html.Div([
                        # #html.H1('The Warming & Distributive Justice dashboard', className="app-header--title", style={'textAlign': 'left'}),
                        # #html.Img(src='/assets/W&R_2.png', className="dashboard-image"),
                        # html.H1("The dashboard's structure"),
                        # html.P([
                        #     '''The dashboard contains six pages which can be navigated between by clicking on links at the top of each page.''', html.Br(),html.Br(),''' 
                        #     Pages 2-4 focus on answering the following three sub RQs:''', html.Br(),html.Br(),'''        
                        #     Page 1 (Introduction) provides background information about the dashboard, how and why it has been developed and the RQs that the dashboard has helped answer.''', html.Br(),html.Br(),'''   
                        #     Page 2 (Contributions to warming) provides a series of dropdown boxes to the left-hand-side of the page. This is where you can select different options and have graphs on the right-hand-side of the page update.''', html.Br(),html.Br(),'''   
                        #     Page 3 (Distributing costs) provides a series of options on the left-hand-side of the page. This is where a user can select different options to answer RQ2.''', html.Br(),html.Br(),'''
                        #     Page 4 (Distributing rights) provides a series of options...''', html.Br(),html.Br(),'''
                        #     Page 5 (Methodology)...''', html.Br(),html.Br(),'''
                        #     Page 6 (Further reading and references)...''', html.Br(),html.Br(),html.Br(),'''     

                        #     The dashboard has been developed with the target audiences of climate negotiators and policymakers in mind, who will continue grappling with these questions and possible equitable effort-sharing approaches for addressing climate change at the country-level.'''], style={'textAlign': 'left'}
                        #     ),
                        # # html.Button("Update"),
                        # ], id='mid-container')
                ]
            )
        ]
    )
])

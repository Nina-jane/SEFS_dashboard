# Import libraries
import dash
from dash import Dash, dcc, html
import os

thisPath = os.path.abspath(os.path.dirname(__file__))
print(dash.__version__)
app = Dash(__name__, use_pages=True)

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

if __name__ == "__main__":
    app.run(debug=True)
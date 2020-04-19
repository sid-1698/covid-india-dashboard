import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from pathlib import Path
import tsplot
import os
import demographics
import statistics
import trajplot
import dailycases
import deepdive
import geoplot 
import json

state = 'India'
path = Path(os.path.dirname(os.path.abspath(' ')))/'Data'

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server()

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#dbdbdb",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Img(
            src = app.get_asset_url('Logo.png'),
            id = 'covid-logo',
            style ={
                'height':'60px',
                'width' : 'auto',
                'margin-bottom':'25px'
            }
        ),
        html.Hr(),
        html.H3(
            "Visualisation Dashboard", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/page-1", id="page-1-link"),
                dbc.NavLink("Trajectory", href="/page-2", id="page-2-link"),
                dbc.NavLink("Daily Cases", href="/page-3", id="page-3-link"),
                dbc.NavLink("Analysis", href="/page-4", id="page-4-link"),
                dbc.NavLink("Geoplot", href="/page-5", id="page-5-link")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

cases = [
    dbc.CardBody(
        [
            html.H5("Cases", className="card-title"),
            html.H6(statistics.cases,
                className="card-text",
            ),
        ]
    ),
]

deaths = [
    dbc.CardBody(
        [
            html.H5("Deaths", className="card-title"),
            html.H6(statistics.deaths,
                className="card-text",
            ),
        ]
    ),
]

recoveries = [
    dbc.CardBody(
        [
            html.H5("Recoveries", className="card-title"),
            html.H6(statistics.recoveries,
                className="card-text",
            ),
        ]
    ),
]

code = {'mh': 'Maharashtra','dl': 'Delhi','tn': 'Tamil Nadu','mp': 'Madhya Pradesh','rj': 'Rajasthan','gj': 'Gujarat','up': 'Uttar Pradesh',
              'tg': 'Telangana','ap': 'Andhra Pradesh','kl': 'Kerala','ka': 'Karnataka','jk': 'Jammu and Kashmir','wb': 'West Bengal',
              'hr': 'Haryana','pb': 'Punjab','br': 'Bihar','or': 'Odisha','ut': 'Uttarakhand','hp': 'Himachal Pradesh','as': 'Assam',
              'ct': 'Chhattisgarh','jh': 'Jharkhand','ch': 'Chandigarh','la': 'Ladakh','an': 'Andaman and Nicobar Islands','ga': 'Goa',
              'py': 'Puducherry','ml': 'Meghalaya','mn': 'Manipur','tr': 'Tripura','mz': 'Mizoram','ar': 'Arunachal Pradesh',
              'dn': 'Dadra and Nagar Haveli','nl': 'Nagaland','dd': 'Daman and Diu','ld': 'Lakshadweep','sk': 'Sikkim','in' :'India'}
              
state_dropdown = dcc.Dropdown(
    id = 'states-ts',
    options = [
       {'label' : value,'value' :key} for key,value in code.items()
    ],
    value='in'
)

home = html.Div([
    dbc.Row(
            [
                dbc.Col(dbc.Card(cases, color="primary", inverse=True)),
                dbc.Col(),
                dbc.Col(dbc.Card(recoveries, color="success", inverse=True)),
                dbc.Col(),
                dbc.Col(dbc.Card(deaths, color="danger", inverse=True)),
                dbc.Col()
            ],
            className="mb-6",
        ),
    html.Br(),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.H2('Exponential Growth !'),width=9),
        dbc.Col(state_dropdown)
    ]),
    dcc.Graph(id='tsplot',figure=tsplot.plot(path,state)),
    html.Br(),
    html.Br(),
    html.H2('Demographics*'),
    dbc.Row([
        dbc.Col(dcc.Graph(id='age-box',figure=demographics.plot2(path)),width=6),
        dbc.Col(dcc.Graph(id='pie',figure=demographics.plot1(path)))
    ]),
    dbc.Row([
        dbc.Col(width=7),
        dbc.Col(html.P('*Most of the data is missing. Although this is believed to be correlatting with the actual values.'))
    ])
])

trajectory = html.Div([
    html.H2('Are we winning ? Compare with other states'),
    html.Hr(),
    html.Div([
        dcc.Dropdown(
        id = 'states-tr',
        options = [
            {'label' : value,'value' : key} for key,value in code.items()
        ],
        value=['in'],
        multi=True
    ),
    html.Button(id='submit-button', n_clicks=0, children='Submit')
    ]),
    dcc.RadioItems(
        id = 'columns-tr',
        options = [
            {'label' : 'Cases', 'value' : 'c'},
            {'label' : 'Deaths', 'value' : 'd'}
        ],
        value = 'c',
        labelStyle = {'display' : 'inline-block'}
    ),
    dcc.Graph(id='trajplot',figure=trajplot.plot(path,['India'],'Confirmed'))
])

daily = html.Div([
    html.H2('Flatten the Curve ?*'),
    html.Hr(),
    dcc.Dropdown(
        id = 'daily-st',
        options = [
            {'label' : value, 'value' : key} for key,value in code.items()
        ],
        value = 'in'
    ),
    dcc.Graph(
        id = 'curve',
        figure = dailycases.plot(path,'India')
    ),
    dbc.Row([
        dbc.Col(width=8),
        dbc.Col(html.P('*SIR Model to follow in the next update'))
    ])
])

heatmap = html.Div([
    html.H2('Geographical Heatmap - Detecting Hotspots'),
    html.Hr(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='india-geo',figure=geoplot.plot1(path)),width=6
        ),
        dbc.Col(
            dcc.Graph(id='state-geo')
        )
    ])
])

analysis = html.Div([
    html.H2('Deepdive'),
    html.P("Let's dive into the actual scenario in different states to understand why they are winning/failing the war."),
    html.Br(),
    html.Hr(),
    dcc.Graph(id='lab', figure=deepdive.plot2(path)),
    dcc.Graph(id='hosp',figure=deepdive.plot1(path))
])




content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id='url'),sidebar,content])


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 6)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return home
    elif pathname == "/page-2":
        return trajectory
    elif pathname == "/page-3":
        return daily
    elif pathname == "/page-4":
        return analysis 
    elif pathname == "/page-5":
        return heatmap
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

app.config['suppress_callback_exceptions'] = True

@app.callback(Output("tsplot",'figure'),[Input('states-ts','value')])
def render_ts_graph(state):
    return tsplot.plot(path,code[state])

app.config['suppress_callback_exceptions'] = True

@app.callback(Output("trajplot",'figure'),[Input('submit-button','n_clicks')],[State('states-tr','value'),State('columns-tr','value')])

def render_traj_graph(clicks,states,column):
    states = [code[item] for item in states]
    if column == 'c':
        return trajplot.plot(path,states,'Confirmed')
    else:
        return trajplot.plot(path,states,'Deceased')  

app.config['suppress_callback_exceptions'] = True

@app.callback(Output("curve",'figure'),[Input('daily-st','value')])

def render_curve(state):
    return dailycases.plot(path,code[state])


app.config['suppress_callback_exceptions'] = True

@app.callback(Output('state-geo','figure'),[Input('india-geo','clickData')])

def render_state_geo(hoverData):
    if not hoverData:
        return dash.no_update
    else:
        return geoplot.plot2(path,hoverData['points'][0]['location'])

if __name__ == "__main__":
    app.run_server()  
from dash import html
import dash
import dash

dash.register_page(__name__)
layout = html.Div([
    html.H1('About Page'),
    html.P('This is the About Page')
])

from dash import html, Dash, dcc, callback, Input, Output, State, dash_table
import pathlib
import pandas as pd
import os
from components import tables
import plotly.express as px


app = Dash(
	meta_tags=[
		{
			'name':'viewport',
			'content':'width=device-width, initial-scale=1.0'
		}
	]
)

app.title = 'Oil and Gas Dashboard'
app.config.suppress_callback_exceptions = True

APP_FOLDER = str(pathlib.Path(__file__).parent.resolve())
file_path = os.path.join(APP_FOLDER, 'data', 'oil-and-gas.parquet')

df = pd.read_parquet(file_path)

#Count total wells for each 'Well Type'
total_wells = df.groupby('Well Type')['Well Name'].count().reset_index(name='Total Wells')

#Count active wells for each 'Well Type'
active_wells = df[df['Well Status'] == 'Active'].groupby('Well Type')['Well Name'].count().reset_index(name='Active Wells')


#Add column for percentage of active wells
df_1 = pd.merge(total_wells, active_wells, on='Well Type')
df_1['% Active Wells'] = (df_1['Active Wells'] / df_1['Total Wells']) * 100

df_1 = df_1[['Well Type','Total Wells','% Active Wells']]

#Total Produced
df_oil = df.groupby('Reporting Year')['Oil Produced, bbl'].sum().reset_index(name='Total Oil Produced')
df_gas = df.groupby('Reporting Year')['Gas Produced, MCF'].sum().reset_index(name='Total Gas Produced')
df_water = df.groupby('Reporting Year')['Water Produced, bbl'].sum().reset_index(name='Total Water Produced')
df_2 = pd.merge(df_oil, df_gas, on='Reporting Year')
df_2 = pd.merge(df_2, df_water, on='Reporting Year')
df_2 = df_2[['Reporting Year','Total Oil Produced','Total Gas Produced','Total Water Produced']]

server = app.server
def build_banner():
	return html.Div(
		id='banner',
		className='banner',
		children = [html.Div(
			id='banner-text',
			 children = [
				html.H5('OIL AND GAS DASHBOARD'),
				html.H6('Productivity and Viability Reporting'),
			]
		),
		html.Div(
			id='banner-logo',
			children=[
				html.A(
					html.Button('ABOUT HENRY')
				),
				html.Button(
					id='learn-more-button', 
					children='HELP',
					n_clicks=0
				),
				html.A(
					html.Img(id='logo', src=app.get_asset_url('dash-logo-new.png'))
				)
			]
		)
		]

		   
		)

def build_tabs():
	return html.Div(
		id='tabs',
		className='tabs',
		children=[
			dcc.Tabs(
				id='app-tabs',
				value='tab2',
				className='custom-tabs',
				children=[
					dcc.Tab(
						id='Stats-tab',
						label='QUICK STATS',
						value='tab1',
						className='custom-tab',
						selected_className='custom-tab--selected'
					),
					dcc.Tab(
						id='Control-chart-tab',
						label='Production Charts Dashboard',
						value='tab2',
						className='custom-tab',
						selected_className='custom-tab--selected'
					)
				]
			)
		]
	)

def build_tab1():
	return [
		html.Div(
			id='set-stats-intro-container',
			children=html.P(
				'Demo dashboard powered by Plotly Dash and hosted on Azure'
			)
		),
		html.Div(
			id='main-body-container',
			children=
			[
				tables.build_table1(df_1),
				tables.build_table2(df_2),
			   
			]
		)
	]
	
def build_tab2():
	return [

		html.Div(
			id='main-chart-container',
			children=[
				tables.dropdowns(df),
				dcc.Graph(id='chart-container'),
			]
		),
		
	]
	

app.layout = html.Div(
	id='big-app-container',
	children=[
		build_banner(),
		html.Div(
			id='app-container',
			children=[
				build_tabs(),
				#Main app
				html.Div(id='app-content')
			]
		),
		
	]
)

@callback(
	Output('app-content', 'children'),
	Input('app-tabs', 'value')
)
def render_tab_content(tab_switch):
	if tab_switch == 'tab1':
		return build_tab1()
	
	return build_tab2()

#dynamically populate dropdown 2 and 3 based on dropdown 1
years = df['Reporting Year'].unique().tolist()
years.sort()
well_names = df['Well Name'].unique().tolist()
well_names.sort()

@callback(
		Output('well-name-dropdown', 'options'),
		Input('well-type-dropdown', 'value')
)
def update_options(value):
	new_df = df[df['Well Type'] == value]
	well_names = new_df['Well Name'].unique().tolist()
	well_names.sort()
	well_names_options = [{'label': item, 'value': item} for item in well_names]

	return well_names_options  


#Generate graph
@callback(
		Output('chart-container', 'figure'),
		Input('submit-button', 'n_clicks'),
		State('well-type-dropdown', 'value'),
		State('well-name-dropdown', 'value'),
)
def update_graph(clicks, well_type, well_name):
	new_df = df[(df['Well Name'] == well_name) & (df['Well Type'] == well_type)]
	new_df = new_df.groupby('Reporting Year')['Gas Produced, MCF'].sum().reset_index(name='Gas Produced, MCF')
	fig = px.line(new_df, x='Reporting Year', y='Gas Produced, MCF', title='Yearly Gas Produced')
	fig.update_layout(
		template="plotly_dark",
		font_color="#95969a",
		width=800,
		height=500,
		title_x=0.5,
		
	)

	fig.update_traces(
		line=dict(color='gold'),
		mode='lines+markers',
		)
	return fig

if __name__ == '__main__':
	app.run_server(debug=True)

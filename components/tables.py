from dash import html, dcc, callback, Input, Output
import helpers
import dash_daq as daq

def build_table1(data):
	data_list = helpers.flattern_list(data.values.tolist())
	html_list = []
	
	for idx,item in enumerate(data_list, start=1):
		if idx % 3 == 0:
			html_list.append(
				html.Div(
					children=[
							daq.GraduatedBar(
									className='daq-graduatedbar',
									max=100,
									size='100px',
									value=int(item),
									showCurrentValue=True,
									color='green' if int(item) > 50 else 'red',
								)
						]
					)
				)
			continue
			
		html_list.append(html.P(item))
	return html.Div(
		id='table1',
		className='table-headers',
		children=[
			html.P('Well Type', className='table-header'),
			html.P('Total Wells', className='table-header'),
			html.P('Active Wells %', className='table-header'),
		] + html_list
	)

def build_table2(data):
	data_list = helpers.flattern_list(data.values.tolist())

	html_list = [html.P(item) for item in data_list]
	return html.Div(
		id='table2',
		className='table-headers',
		children=[
			html.P('Year', className='table-header'),
			html.P('Total Oil Produced', className='table-header'),
			html.P('Total Gas Produced', className='table-header'),
			html.P('Total Water Produced', className='table-header'),
		] + html_list
	)

def dropdowns(df):
	well_types = df['Well Type'].unique().tolist()
	well_types.sort()
	well_names = df['Well Name'].unique().tolist()
	well_names.sort()

	return html.Div(
		id='dropdowns',
		className='dropdowns',
		children=[
			html.Div(
				id='dropdown1',
				className='dropdown',
				children=[
					html.P(
						id='dropdown1-text',
						children='Select a Well Type'
					),
					dcc.Dropdown(
						id='well-type-dropdown',
						options=[
							 {'label': item, 'value': item} for item in well_types
						],
						value='Gas Development',
						className='dropdown-items'
					)
				]
			),

			html.Div(
				id='dropdown3',
				className='dropdown',
				children=[
					html.P(
						id='dropdown3-text',
						children='Select a Well Name'
					),
					dcc.Dropdown(
						id='well-name-dropdown',
						className='dropdown-items'
					)
				]
			),
			html.Button(
				id='submit-button',
				children='Submit',
				n_clicks=0,
				className='submit-button'
			)
		]
	)

def build_graph():
	return dcc.Graph(
		id='chart-container',
	)



# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label':'All Sites', 'value':'ALL'},
                                                {'label':'VAFB SLC-4E', 'value':'OPT1'},
                                                {'label':'KSC LC-39A', 'value':'OPT2'},
                                                {'label':'CCAFS SLC-40', 'value':'OPT3'},
                                                {'label':'CCAFS LC-40', 'value':'OPT4'}                                            
                                            ],value='ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site                                
                                html.Div(dcc.Graph(
                                    id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload,max_payload],
                                    marks={
                                    0: '0',
                                    2500: '2500',
                                    5000: '5000',
                                    7500: '7500',
                                    10000: '10000'
                                    },
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(
                                    id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

def get_pie(launch_site):
    nameList = [0,1]
    if launch_site == 'ALL':
        pie_data = spacex_df.groupby('Launch Site')['class'].mean().reset_index()
        fig = px.pie(pie_data, values=pie_data['class'], names=pie_data['Launch Site'], title='% of successul launch by launch sites')
    elif launch_site == 'OPT1':
        df = spacex_df.loc[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        fig = px.pie(df, values=df['class'].value_counts(), names=nameList, title='% of successul launch by VAFB SLC-4E')
    elif launch_site == 'OPT2':
        df = spacex_df.loc[spacex_df['Launch Site'] == 'KSC LC-39A']
        fig = px.pie(df, values=df['class'].value_counts(), names=nameList, title='% of successul launch by KSC LC-39A')
    elif launch_site == 'OPT3':
        df = spacex_df.loc[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        fig = px.pie(df, values=df['class'].value_counts(), names=nameList, title='% of successul launch by CCAFS SLC-40')
    else:
        df = spacex_df.loc[spacex_df['Launch Site'] == 'CCAFS LC-40']
        fig = px.pie(df, values=df['class'].value_counts(), names=nameList, title='% of successul launch by CCAFS LC-40')

    return fig 
    
         


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value'))

def get_scatter(launch_site, payload):
    if launch_site == 'ALL':
        fig = px.scatter(spacex_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    elif launch_site == 'OPT1':
        df = spacex_df.loc[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    elif launch_site == 'OPT2':
        df = spacex_df.loc[spacex_df['Launch Site'] == 'KSC LC-39A']
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    elif launch_site == 'OPT3':
        df = spacex_df.loc[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    else:
        df = spacex_df.loc[spacex_df['Launch Site'] == 'CCAFS LC-40']
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()

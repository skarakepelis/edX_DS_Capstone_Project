# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline spacex_df into pandas dataframe
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
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', options=[
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                {'label': 'All', 'value': 'All'}
                                ],
                                value='All',
                                placeholder='Select a Launch Site here',
                                searchable=True),
                                html.Br(),
                                #html.Div(id='success-pie-chart'),                               
                                

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    value = [min_payload, max_payload],
                                    step=1000,
                                    marks={0:{'label':'0'},
                                            2500:{'label':'2500'},
                                            5000:{'label':'5000'},
                                            7500:{'label':'7500'},
                                            10000:{'label':'10000'}
                                            }
                                ),                          
                                html.Br(),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')])


def updating_pie(value1):
    if value1=='All':
        per_CCAFS_LC = spacex_df.loc[(spacex_df['Launch Site'] == 'CCAFS LC-40') & (spacex_df['class']==1)].shape[0]
        per_VAFB_SLC = spacex_df.loc[(spacex_df['Launch Site'] == 'VAFB SLC-4E') & (spacex_df['class']==1)].shape[0]
        per_KSC_LC = spacex_df.loc[(spacex_df['Launch Site'] == 'KSC LC-39A') & (spacex_df['class']==1)].shape[0]
        per_CCAFS_SLC = spacex_df.loc[(spacex_df['Launch Site'] == 'CCAFS SLC-40') & (spacex_df['class']==1)].shape[0]
        sum = per_CCAFS_LC + per_VAFB_SLC + per_KSC_LC + per_CCAFS_SLC
        percentages = [round(per_CCAFS_LC/sum*100,1), round(per_VAFB_SLC/sum*100,1), round(per_KSC_LC/sum*100,1), round(per_CCAFS_SLC/sum*100,1)]
        fig = px.pie(values=percentages, names=['CCAFS LC-40','VAFB SLC-4E','KSC LC-39A','CCAFS SLC-40'])
        return fig
    else:
        #filtered_df = spacex_df[spacex_df['Launch Site'] == value1].groupby(['Launch Site', 'class']). \
        #size().reset_index(name='class count')
        #title = f"Total Success Launches for site {value}"
        #filtered_df = filtered_df
        #fig = px.pie(filtered_df,values='class count', names='class', title=title)
        #return fig
        
        data_clip = spacex_df.loc[spacex_df['Launch Site'] == value1]
        success = np.count_nonzero(data_clip['class']==1)
        failure = np.count_nonzero(data_clip['class']==0)
        sum = success + failure
        percentages = [round(success/sum*100,1), round(failure/sum*100,1)]
        fig2 = px.pie(values=percentages, names=['1','0'])
        return fig2

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")])

def updating_scatterplot(site, value):
    mass_1 = [v for v in value]
    mask = (spacex_df['Payload Mass (kg)']>=mass_1[0]) & (spacex_df['Payload Mass (kg)']<=mass_1[1])
    data_crop = spacex_df.loc[mask]
    if site=='All':
        fig = px.scatter(data_crop, x='Payload Mass (kg)', y='class', color="Booster Version Category")
        #plt.xlabel('Payload Mass (kg)')
        #plt.ylabel('Class')
        return fig
    else:
        data_crop_site = data_crop.loc[data_crop['Launch Site'] == site]
        fig = px.scatter(data_crop, x='Payload Mass (kg)', y='class', color="Booster Version Category")
        #plt.xlabel('Payload Mass (kg)')
        #plt.ylabel('Class')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

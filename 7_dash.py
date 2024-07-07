#import wget
#wget.download("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
#wget.download("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py")


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
options = spacex_df['Launch Site'].unique().tolist()
options.append('All Sites')

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Div(['Select Launch Site', dcc.Dropdown(
                                                                id='site-dropdown', 
                                                                options=options,
                                                                value='All Sites',
                                                                placeholder='Choose a Site')]),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', 
                                                min=min_payload, 
                                                max=max_payload, 
                                                step=500,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(site):
    if site == 'All Sites':
        data = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(data, 
                     names='Launch Site', 
                     values='class',
                     title="Succesful launches for all sites")
    else:
        data = spacex_df.loc[spacex_df['Launch Site'] == site, ['class']].value_counts().to_frame()
        fig=px.pie(data, 
                   names=['Failure', 'Success'], 
                   values='count', 
                   title=f'Total Success Launches by {site} Site')
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)

def get_scatter_chart(site, payload):
    start, stop = payload
    if site == 'All Sites':
        fig = px.scatter(spacex_df, 
                          x='Payload Mass (kg)', 
                          y='class',
                          title='Payload vs Success for all Sites',
                          color='Launch Site')
      
    else:
        data = spacex_df.loc\
            [(spacex_df['Launch Site'] == site) & \
            (spacex_df['Payload Mass (kg)'] <= stop) & \
            (spacex_df['Payload Mass (kg)'] >= start)]         
        
        fig = px.scatter(data,
                        x='Payload Mass (kg)',
                        y='class',
                        title=f'Payload vs Success for {site} Site')
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
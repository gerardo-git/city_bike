################################################ City BikeDASHBOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from streamlit_keplergl import keplergl_static
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'Citi Bike - NYC Trip Analysis', layout='wide')
st.title("Citi Bike - NYC Trip Analysis")

st.markdown("This dashboard is meant to support CitiBike in its data-driven decisions for the bike rental logistics in NYC")
st.markdown("Currently, CitiBike runs into a situation where customers complain about bikes not being available at certain times. This analysis aims to look at the potential reasons behind this and showcase any other areas of opportunity.")

########################## Import data ###########################################################################################

df = pd.read_csv('ny_city_modified_data.csv', index_col = 0)
top20 = pd.read_csv('top20_stations.csv', index_col = 0)

# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart

fig = go.Figure(go.Bar(x = top20['start_station'], y = top20['trips_per_station'], marker={'color': top20['trips_per_station'],'colorscale': 'Greens'}))
fig.update_layout(
    title = {'text': 'Top 20 most popular bike stations in New York','font': {'size': 30, 'color': 'white'}},
    #title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)


## Line chart 

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'],'color': 'dodgerblue'}),
secondary_y = False
)

fig_2.add_trace(
go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'],'color': 'orangered'}),
secondary_y=True
)

fig_2.update_layout(
    title = {'text': 'Daily bike trips and temperatures in 2020','font': {'size': 30, 'color': 'white'}},
    height = 600,

    legend={'font':{'size': 16}}    
)

st.plotly_chart(fig_2, use_container_width=True)


### Add the map from the html file ###

path_to_html = "Kepler Map Top 150 rides.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height=1000)

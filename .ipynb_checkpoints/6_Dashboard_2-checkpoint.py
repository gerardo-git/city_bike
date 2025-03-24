import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerizer import numerize
from PIL import Image

########################### Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'Citi Bike - NYC Trip Analysis', layout='wide')
st.title("Citi Bike - NYC Trip Analysis")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('ny_city_small_data.csv', index_col = 0)

######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("This dashboard is meant to support CitiBike in its data-driven decisions for the bike rental logistics in NYC")
    st.markdown("Currently, CitiBike runs into a situation where customers complain about bikes not being available at certain times. This analysis aims to look at the potential reasons behind this and showcase any other areas of opportunity. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("citi_bike.jpg") #source: https://www.nyc.gov/office-of-the-mayor/news/576-18/mayor-de-blasio-dramatic-expansion-citi-bike
    st.image(myImage)


    ### Create the dual axis line chart page ###
    
elif page == 'Weather component and bike usage':

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
    st.markdown("There is an clear correlation between the rise and drop of temperatures and the frequency of bike trips taken daily. As temperature decreases, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October. The day with maximum bike trips was September 21st and the one with the lowest trips was January 29th")

### Most popular stations page

    # Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(), default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label="Total Bike Rides", value=f"{int(total_rides):,}")


    
    # Bar chart

    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Greens'}))

    fig.update_layout(
    title = {'text': 'Top 20 most popular bike stations in New York','font': {'size': 28, 'color': 'white'}},
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 we can seeW 21 St & 6 Ave, West St & Chambers St as well as Broadway & W 58 St. Only 5 stations have more than 1000 trips and the rest of them are below 1000. These are the most popular stations per season:")
    st.markdown("-Spring: 1 Ave & E 68 St")
    st.markdown("-Summer: West St & Chambers St")
    st.markdown("-Fall: W 21 St & 6 Ave")
    st.markdown("-Winter: W 21 St & 6 Ave")
elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.markdown("Interactive map showing aggregated bike trips over NY City")

    path_to_html = "Kepler Map Top 150 rides.html"

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage - !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  FILTER !!!!!!    WHERE   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    st.header("Top 150 Bike Trips in New York")
    st.components.v1.html(html_data,height=1000)
#    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("#### These were the top 5 most common trips:")
    st.markdown("- Central Park S & 6 Ave - Central Park S & 6 Ave (same station)") 
    st.markdown("- 7 Ave & Central Park South - 7 Ave & Central Park South (same station)")
    st.markdown("-  Roosevelt Island Tramway - Roosevelt Island Tramway (same station)") 
    st.markdown("-  Grand Army Plaza & Central Park S - Grand Army Plaza & Central Park S (same station)")
    st.markdown("-  W 21 St & 6 Ave - 9 Ave & W 22 St")
    st.markdown("The first 4 trips are round trips where the starting station is the same as the final station. Only the 5th most common trip is between 2 different stations. This means we should consider both important stations with round trips and also hub stations")
    st.markdown("We can detect from the map that there are some sort of hubs or points where there are more stations and trips. The first one is along the 1st Avenue between East 84th Street and East 62nd. This area has several stations and trips that are interconnected which could be prioritized. It also contains the most common station overall 1 Ave & E 68 St. The most common trip in the dataset is the one starting in 6th Ave & Central Park S station and ending in the same station. This means these clients are renting a bike to take a ride in the park or the vicinity. This could be labelled as the most important station and should be well stock by all means. Other hubs that contain several stations and trip pairs are the Lenox Hill and the Central Park hubs. They should also be prioritized.")

else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("Citi_bike_single.png")  #source: https://www.glenwoodnyc.com/manhattan-living/citibike-bike-rental-nyc/
    st.image(bikes)
    st.markdown("### Our analysis has shown that CitiBike should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations around the water line, such as heater on the Lake, Streeter Dr/Grand Avenue, Millenium Park, Columbus Dr/Randolph Street, Shedd Aquarium, Michigan Avenue/Oak Street, Canal Street/Adams Street")
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but provide a lower supply in winter and late autumn to reduce logistics costs")
import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

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
df_starting_time = pd.read_csv('df_starting_time.csv', index_col = 0)

######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("This dashboard is meant to support CitiBike in its data-driven decisions for the bike rental logistics in NYC")
    st.markdown("Currently, CitiBike runs into a situation where customers complain about bikes not being available at certain times. This analysis aims to look at the potential reasons behind this and showcase any other areas of opportunity. The dashboard is separated into 4 sections:")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Most popular stations")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

#source: https://www.nyc.gov/office-of-the-mayor/news/576-18/mayor-de-blasio-dramatic-expansion-citi-bike
    st.image("citi_bike.jpg")


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
    title = {'text': 'Daily bike trips and temperatures in 2022','font': {'size': 30, 'color': 'white'}},
    height = 600,

    legend={'font':{'size': 16}}    
)
    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("There is a clear correlation between the rise and drop of temperatures and the frequency of bike trips taken daily. As temperature decreases, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")
    st.markdown("The day with maximum bike trips was September 21st and the one with the lowest trips was January 29th")


    fig_t = go.Figure(go.Bar(x = df_starting_time['started_at'], y = df_starting_time['value'], marker={'color':df_starting_time['value'],'colorscale': 'Blues'}))

    fig_t.update_layout(
    title = {'text': 'Hourly Distribution of Bike Trips','font': {'size': 28, 'color': 'white'}},
    xaxis=dict(
        title='Time of Day (Hour)',
        tickmode='linear',
        tick0=0,
        dtick=1
    ),
    yaxis_title ='Total trips',
    width = 1400, height = 600
)
    st.plotly_chart(fig_t, use_container_width=True)
    st.markdown("The chart shows the hourly distribution of bike trips in New York, revealing clear usage patterns tied to daily routines.")
    st.markdown("There’s a **morning surge between 7 AM and 9 AM**, peaking at **8 AM**, which likely reflects commuters heading to work or school. Afterwards, usage remains **steady through the midday hours (10 AM – 3 PM)**, suggesting trips for errands, leisure, or flexible work schedules.")
    st.markdown("The **highest volume occurs between 4 PM and 7 PM**, with a sharp peak at **5 PM**, aligning with the evening commute. This is the most active period of the day for bike usage.")
    st.markdown("After 7 PM, trip counts **gradually decline**, and activity drops significantly **after 9 PM**, reaching the lowest levels between **12 AM and 5 AM**, likely due to reduced demand and safety concerns.")
    st.markdown("Overall, the chart reflects a **typical commuter-driven pattern**, highlighting the importance of bike-sharing systems as a key part of New York City’s daily transportation—especially during rush hours.")



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

    path_to_html = "Kepler_Map_Top_150_rides.html"

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage 
    st.header("Top 150 Bike Trips in New York")
    st.components.v1.html(html_data,height=1000)
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
#source: https://www.glenwoodnyc.com/manhattan-living/citibike-bike-rental-nyc/
    st.image("Citi_bike_single.png")
    st.markdown("### Our analysis has shown that CitiBike should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations in the specific hubs where the top 150 trips are grouped.")
    st.markdown("- Adjust the bike stock seasonally. Less bikes on colder months and more bikes on warmer months. This reduces the operating costs and the general decay of bikes during the winter months.")
    st.markdown("- Consider that some stations in touristic spots may not need to be interconnected but it is still a good idea to cover them. People may want to take a ride around a park near the suburbs recreationally even if this ride was a simple round trip.")
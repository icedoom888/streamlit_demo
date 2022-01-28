import pandas as pd
import numpy as np
import json
from geopy.geocoders import Nominatim
import requests
import folium
import streamlit as st
from streamlit_folium import folium_static
import branca


st.title('World Population')

def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)/1000000

@st.cache
def load_data():
    df = pd.read_csv('population_total.csv')
    df = df.set_index('country')
    df.index.name = None
    for country in df.index:
        df.loc[country] = df.loc[country].map(lambda x: convert_str_to_number(x))

    df = df.T
    df.index = df.index.map(int)

    return df.T

# Function to retrieve coordinates of city
def center():
   address = 'Surabaya, ID'
   geolocator = Nominatim(user_agent="id_explorer")
   location = geolocator.geocode(address)
   latitude = location.latitude
   longitude = location.longitude
   return latitude, longitude


def show_maps(map_sby, data_geo, data, threshold_scale):

    maps = folium.Choropleth(geo_data = data_geo,
                             data = data,
                             columns=['Country', 'Population'],
                             key_on='feature.properties.name',
                             threshold_scale=threshold_scale,
                             fill_color='YlOrRd',
                             fill_opacity=0.7,
                             line_opacity=0.2,
                             legend_name='Population').add_to(map_sby)

    folium_static(map_sby)

# Load data
df = load_data()
countries = df.index
data_geo = json.load(open('world_map.json'))

# Pick a year sidebar
year = st.sidebar.slider('Pick a year', min_value=min((df.T.index.tolist())), max_value=max((df.T.index.tolist())))
y_data = df.loc[:, year]
y_data.columns = ['Country', 'Population']

# What do you see
select_data = st.sidebar.radio("What normalisation do you want?", ["Year", "All-time"])
if select_data == "Year":
    threshold_scale = np.linspace(y_data.min(),
                                  y_data.max(),
                                  10,
                                  dtype=float)
    colorscale = branca.colormap.linear.YlOrRd_09.scale(y_data.min(), y_data.max())

elif select_data == "All-time":
    threshold_scale = np.linspace(df.min(axis=1).min(),
                                  df.max(axis=1).max(),
                                  10,
                                  dtype=float)
    colorscale = branca.colormap.linear.YlOrRd_09.scale(df.min(axis=1).min(), df.max(axis=1).max())

# showing the maps
map_sby = folium.Map(tiles='OpenStreetMap', max_bounds=True)

show_maps(map_sby, data_geo, y_data, threshold_scale)
import streamlit as st
import pandas as pd
import numpy as np

st.title('World Population')


def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)

# Load data
@st.cache
def load_data():
    df = pd.read_csv('population_total.csv')
    df = df.set_index('country')
    df.index.name = None
    for country in df.index:
        df.loc[country] = df.loc[country].map(lambda x: convert_str_to_number(x))
    return df

data = load_data()
countries = data.index

sel_countries = st.multiselect('Select a Country', countries)
c_data = data.loc[sel_countries].T
c_data.index = c_data.index.map(int)

st.area_chart(data=c_data)



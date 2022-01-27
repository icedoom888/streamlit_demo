import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data as vd


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

    df = df.T
    df.index = df.index.map(int)

    return df.T

data = load_data()
countries = data.index
year = st.slider('Pick a year', min_value=min((data.T.index.tolist())), max_value=max((data.T.index.tolist())))
y_data = data.loc[:, year]

topo = alt.topo_feature(vd.world_110m.url, 'countries')
source = y_data

chart = alt.Chart(topo).mark_geoshape().encode(
    color='rate:Q')
# ).transform_lookup(
#     lookup='id',
#     from_=alt.LookupData(source, 'id', ['rate'])
# ).project(
#     type='equirectangular'
# ).properties(
#     width=500,
#     height=300
# )

st.altair_chart(chart)
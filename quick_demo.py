import streamlit as st
import pandas as pd
import numpy as np

st.title('World Population')

# Load data
@st.cache
def load_data():
    df = pd.read_csv('population_total.csv')
    df = df.set_index('country')
    return df

data = load_data()
countries = data.index

country = st.selectbox('Select a Country', countries)

c_data = data.loc[country]
with st.container():
    st.write(f"Showing {country} population data")
    # You can call any Streamlit command, including custom components:
    st.area_chart(data=c_data)



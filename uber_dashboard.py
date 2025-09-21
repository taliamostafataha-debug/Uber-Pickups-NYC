# uber_dashboard.py

import streamlit as st
import pandas as pd
import ssl
import plotly.express as px

# --- SSL fix for macOS ---
ssl._create_default_https_context = ssl._create_unverified_context

# --- 1️⃣ Page Setup ---
st.set_page_config(
    page_title="NYC Uber Pickups Dashboard",
    layout="wide"
)

st.title("NYC Uber Pickups Dashboard")
st.markdown("""
This dashboard shows Uber pickups in New York City. 
You can explore patterns over time and by hour using the interactive widgets below.
""")

# --- 2️⃣ Data Source ---
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# --- 3️⃣ Load Data Function with Caching ---
@st.cache_data
def load_data(nrows=10000):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.columns = [str(col).lower() for col in data.columns]
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# --- 4️⃣ Load Data ---
data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache_data)")

# --- 5️⃣ Show Raw Data ---
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.dataframe(data.head())

# --- 6️⃣ Visualization 1: Pickups by Hour (Line Chart) ---
st.subheader("Pickups by Hour")
hour_counts = data[DATE_COLUMN].dt.hour.value_counts().sort_index()
fig_hour = px.line(
    x=hour_counts.index,
    y=hour_counts.values,
    labels={'x':'Hour of Day', 'y':'Number of Pickups'},
    title="Total Uber Pickups by Hour"
)
st.plotly_chart(fig_hour, use_container_width=True)
st.markdown("**Insight:** Pickups tend to be higher during rush hours and lower at night.")

# --- 7️⃣ Visualization 2: Map of Pickups with Hour Filter ---
st.subheader("Pickups Map by Hour")
selected_hour = st.slider("Select hour of the day", 0, 23, 12)
filtered_data = data[data[DATE_COLUMN].dt.hour == selected_hour]

st.markdown(f"Displaying {len(filtered_data)} pickups between {selected_hour}:00 and {selected_hour}:59")
st.map(filtered_data[['lat', 'lon']])

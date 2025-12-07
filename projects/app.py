import streamlit as st
import pandas as pd
from core import load_data, plot_time_series

# Initial configuration of the Dashboard
st.set_page_config(page_title="Arizona Grassland Ecohydrology Dashboard", layout="wide")

st.title("🌵 Arizona Grassland Ecohydrology Dashboard")
st.markdown("""
This dashboard visualizes monthly ecohydrological conditions from the **AmeriFlux US-SRG (Santa Rita Grassland)** site,
merged with **OpenET** satellite evapotranspiration estimates.

Use the sidebar controls to select the time window and variables to analyze.
""")

# Load data
df = load_data()

# Sidebars
st.sidebar.header("Filters")

# Selecting year's range
min_year = int(df["Date"].dt.year.min())
max_year = int(df["Date"].dt.year.max())

year_range = st.sidebar.slider(
    "Select year range:", min_value=min_year, max_value=max_year, value=(min_year, max_year)
)

# Filtering dataset
df_filtered = df[(df["Date"].dt.year >= year_range[0]) & (df["Date"].dt.year <= year_range[1])]

# Selecting variables
numeric_cols = [col for col in df.columns if df[col].dtype != "object" and col != "Date"]

variables = st.sidebar.multiselect(
    "Variables to display:", options=numeric_cols, default=["AirTemp_C", "VPD_kPa", "ET_mm_month"]
)

# Timeseries graphic
st.subheader("📈 Time Series of Selected Variables")

if len(variables) == 0:
    st.warning("Please select at least one variable.")
else:
    fig = plot_time_series(df_filtered, variables)
    st.plotly_chart(fig, use_container_width=True)

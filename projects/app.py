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

# Variable list
pretty_choices = {
    "AirTemp_C": "Air Temperature (°C)",
    "VPD_kPa": "Vapor Pressure Deficit (kPa)",
    "SoilTemp_10cm_C": "Soil Temperature 10 cm (°C)",
    "SoilH2O_m3m3": "Soil Moisture (m³/m³)",
    "Wind_speed_ms": "Wind Speed (m/s)",
    "RelHum_%": "Relative Humidity (%)",
    "Rain_mm": "Rainfall (mm)",
    "SolarRad_kWm2": "Solar Radiation (kW/m²)",
    "ET_mm_month": "Evapotranspiration (mm/month)"
}

# List of variable keys
var_options = list(pretty_choices.keys())

# Primary Y-axis
y1_var = st.sidebar.selectbox(
    "Primary Y-axis variable:",
    var_options,
    index=0
)

# Secondary Y-axis
y2_var = st.sidebar.selectbox(
    "Secondary Y-axis variable:",
    var_options,
    index=1
)

# Time filter
min_year = int(df["Date"].dt.year.min())
max_year = int(df["Date"].dt.year.max())

year_range = st.sidebar.slider(
    "Select year range:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Filtering dataset
df_filtered = df[(df["Date"].dt.year >= year_range[0]) &
                 (df["Date"].dt.year <= year_range[1])]


# Timeseries graphic
st.subheader("📈 Time Series of Selected Variables")

fig = plot_time_series(df_filtered, y1_var, y2_var)
st.plotly_chart(fig, use_container_width=True)

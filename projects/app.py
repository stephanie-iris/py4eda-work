import streamlit as st
import pandas as pd
from core import load_data, plot_time_series, plot_correlation, compute_correlation, plot_corr_matrix

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

pretty_to_key = {v: k for k, v in pretty_choices.items()}

# Primary Y-axis
y1_pretty = st.sidebar.selectbox(
    "Primary Y-axis variable:",
    list(pretty_choices.values())
)
y1_var = pretty_to_key[y1_pretty]

# Secondary Y-axis
y2_pretty = st.sidebar.selectbox(
    "Secondary Y-axis variable:",
    ["None"] + list(pretty_choices.values())
)
y2_var = pretty_to_key[y2_pretty] if y2_pretty != "None" else "None"

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
st.pyplot(fig)


st.subheader("🔍 Relationship Between Selected Variables")

# Prevent None in secondary axis
if y2_var == "None":
    st.info("Select a secondary variable to compute correlation.")
else:
    # Plot correlation graph
    corr_fig = plot_correlation(df_filtered, y1_var, y2_var)
    st.pyplot(corr_fig)

    # Compute correlation
    corr_value = compute_correlation(df_filtered, y1_var, y2_var)

    # Print correlation text
    st.markdown(
        f"""
        **Pearson correlation between {pretty_choices[y1_var]} and {pretty_choices[y2_var]}:**  
        `r = {corr_value:.3f}`
        """
    )


show_matrix = st.checkbox("Show full Pearson correlation matrix")

if show_matrix:
    st.subheader("📊 Correlation Matrix (optional)")
    fig_corr = plot_corr_matrix(df_filtered)
    st.pyplot(fig_corr)

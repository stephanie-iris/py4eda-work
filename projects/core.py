# core.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data():
    df = pd.read_pickle("./projects/data/processed/US_SRG_merged_clean.pkl")
    # garantir que Date é datetime
    df["Date"] = pd.to_datetime(df["Date"])
    return df

# Dictionary with pretty variable names
pretty_names = {
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

def plot_time_series(df, variables):
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    # Colors
    colors = sns.color_palette("tab10", len(variables))
    first_var = variables[0]

    if first_var == "Rain_mm":
        ax1.bar(
            df["Date"],
            df[first_var],
            color=colors[0],
            alpha=0.35,
            width=20,
            label=pretty_names[first_var]
        )
    else:
        sns.lineplot(
            data=df,
            x="Date",
            y=first_var,
            ax=ax1,
            label=pretty_names[first_var],
            color=colors[0]
        )

    ax1.set_ylabel(pretty_names[first_var])

    secondary_vars = variables[1:]

    for i, var in enumerate(secondary_vars, start=1):

        if var == "Rain_mm":
            ax2.bar(
                df["Date"],
                df[var],
                color=colors[i],
                alpha=0.3,
                width=20,
                label=pretty_names[var]
            )
        else:
            sns.lineplot(
                data=df,
                x="Date",
                y=var,
                ax=ax2,
                label=pretty_names[var],
                color=colors[i]
            )

    # Dynamic label for secondary axis
    if len(secondary_vars) == 1:
        ax2.set_ylabel(pretty_names[secondary_vars[0]])
    elif len(secondary_vars) > 1:
        ax2.set_ylabel("Secondary variables")
    else:
        ax2.set_ylabel("")

    # Merge legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="upper left"
    )

    ax1.set_title("Ecohydrological Variables Over Time")
    fig.tight_layout()
    return fig

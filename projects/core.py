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

def plot_time_series(df, primary_var, secondary_var):
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    # Colors
    colors = sns.color_palette("tab10", 2)

    if primary_var == "Rain_mm":
        ax1.bar(
            df["Date"],
            df[primary_var],
            color=colors[0],
            alpha=0.35,
            width=20,
            label=pretty_names[primary_var]
        )
    else:
        sns.lineplot(
            data=df,
            x="Date",
            y=primary_var,
            ax=ax1,
            label=pretty_names[primary_var],
            color=colors[0]
        )

    ax1.set_ylabel(pretty_names[primary_var])

    if secondary_var != "None":      
        
        if secondary_var == "Rain_mm":
            ax2.bar(
                df["Date"],
                df[secondary_var],
                color=colors[1],
                alpha=0.3,
                width=20,
                label=pretty_names[secondary_var]
            )
        else:
            sns.lineplot(
                data=df,
                x="Date",
                y=secondary_var,
                ax=ax2,
                label=pretty_names[secondary_var],
                color=colors[1]
            )

        ax2.set_ylabel(pretty_names[secondary_var])
    else:
        ax2.set_ylabel("")    # empty without Y2
    
    # REMOVE secondary-axis legend (fix)
    if ax2.get_legend() is not None:
        ax2.get_legend().remove()

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

def plot_correlation(df, var_x, var_y):
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Scatter + regression line
    sns.regplot(
        data=df,
        x=var_x,
        y=var_y,
        scatter_kws={"alpha": 0.4},
        ax=ax
    )

    # Axis labels using pretty names
    ax.set_xlabel(pretty_choices[var_x])
    ax.set_ylabel(pretty_choices[var_y])

    # Title
    ax.set_title(f"Relationship Between {pretty_choices[var_x]} and {pretty_choices[var_y]}")

    fig.tight_layout()
    return fig

def compute_correlation(df, var_x, var_y):
    # Compute Pearson correlation
    corr_value = df[[var_x, var_y]].corr().iloc[0, 1]
    return corr_value


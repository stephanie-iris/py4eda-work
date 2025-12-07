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


def plot_time_series(df, variables):
    # Create figure and primary axis
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    # Choose colors
    colors = sns.color_palette("tab10", len(variables))

    first_var = variables[0]

    if first_var == "Rain_mm":
        # Rain plotted as bars
        ax1.bar(
            df["Date"],
            df["Rain_mm"],
            color=colors[0],
            alpha=0.35,
            label=f"{first_var} (bar)",
            width=20,
        )
    else:
        # Regular line plot
        sns.lineplot(data=df, x="Date", y=first_var, ax=ax1, label=first_var, color=colors[0])

    ax1.set_ylabel(first_var)
    ax1.set_xlabel("Date")

    for i, var in enumerate(variables[1:], start=1):
        if var == "Rain_mm":
            # Rain always as bar
            ax2.bar(
                df["Date"],
                df["Rain_mm"],
                color=colors[i],
                alpha=0.30,
                label=f"{var} (bar)",
                width=20,
            )
        else:
            # Line plot for numeric variables
            sns.lineplot(data=df, x="Date", y=var, ax=ax2, label=var, color=colors[i])

    ax2.set_ylabel("Secondary variables")

    lines_ax1, labels_ax1 = ax1.get_legend_handles_labels()
    lines_ax2, labels_ax2 = ax2.get_legend_handles_labels()

    ax1.legend(lines_ax1 + lines_ax2, labels_ax1 + labels_ax2, loc="upper left")

    # Title
    ax1.set_title("Ecohydrological Variables Over Time")

    fig.tight_layout()
    return fig

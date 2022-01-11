import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from pathlib import Path
import matplotlib as mpl

BLUE = "#0059ff"
GOLD = "#fdbd28"
GREEN = "#28D9AA"
RED = "#EE5149"
METAL_SUN = "#AD8D40"
DARK_ORCHID = "#9A34D1"
MAGENTA = "#8A4859"
OXFORD = "#121C3B"
PINK = "#DB9995"
GREY = "#788995"

def format_bitdotio(fig,
                    title="Add Title",
                    rect=[0.02,0.1,0.97,0.9],
                    text="Add Text",
                    logo_path="../resources/logo.png",
                    twitter_path="../resources/twitter.png",):
    """Utility function for applying bit.io formatting"""
    fig.tight_layout(rect=rect)
    if text:
        fig.text(0.1, 0.05, text, ha='left',
            fontdict={"family":"Inter", "size":8, "color":GREY})
    if title:
        fig.suptitle(title, x=0.1, y=0.96,
                    fontweight="bold", ha="left", fontdict={"family":"Inter", "size":8, "color":"black", "alpha":0.8})
    if logo_path:
        logo=Image.open(logo_path)
        logo_ax = plt.axes([0.8,0.88, 0.13, 0.13], frameon=True) 
        logo_ax.imshow(logo)
        logo_ax.axis('off')
        logo_ax.patch.set_facecolor("white")
    if twitter_path:
        twitter=Image.open(twitter_path)
        twt = plt.axes([0.8,0.0, 0.13, 0.13], frameon=True) 
        twt.imshow(twitter)
        twt.axis('off')
        fig.patch.set_facecolor("white")
    fig.patch.set_facecolor("white")
    
    return fig



def labor_turnover_rates(layoffs_data, quits_data, openings_data, recessions_data, save=False, show=True):
    """
    Plot labor turnover rates.
    """
    plt.style.use("../resources/bitdotio.mplstyle")
    fig, ax = plt.subplots(figsize=(8, 4))

    # Plot Lines
    ax.plot(layoffs_data.date, layoffs_data.value, c=RED, linewidth=2, label="Layoffs/Discharges")
    ax.plot(quits_data.date, quits_data.value, c=BLUE, linewidth=2, label="Quit Rate")
    ax.plot(openings_data.date, openings_data.value, c=GREEN, linewidth=2, label="Job Openings")

    # Plot Recessions
    ax.fill_between(recessions_data['date'], 0,1, where=recessions_data['value']==1, transform=ax.get_xaxis_transform(),
                    alpha=0.2, facecolor=GREY, linewidth=0)

    # Labels
    ax.set_xlabel("Date")
    ax.set_ylabel("Rate")

    # format y axis percent
    ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter(xmax=100))

    # extend xrange
    ax.set_xlim(left=pd.Timestamp("2003-01-01"), right=pd.Timestamp("2023-12-31"))

    # labels at end of lines
    labels = ["Job Openings", "Quits", "Layoffs/Discharges"]
    x = pd.to_datetime("today")
    y = [6.5, 2.9, 0.8]
    colors = [GREEN, BLUE, RED]
    for i, label in enumerate(labels):
        ax.annotate(text=label, xy=(x, y[i]), xytext=(x,y[i]), textcoords="data", color=colors[i], fontsize=8, fontweight="bold")

    ax.annotate(text = "2007-09\nRecession", xy=(pd.to_datetime("2007-12-20"), 4.1), xytext=(pd.to_datetime("2007-12-20"), 4.1), textcoords="data", color=GREY, fontsize=7)
    ax.annotate(text = "COVID-19 Recession", xy=(pd.to_datetime("2020-02-01"), 0.1), xytext=(pd.to_datetime("2020-02-01"), 0.1), textcoords="data", color=GREY, fontsize=7, horizontalalignment="right")

    # Formatting
    ## Ticks
    ax.tick_params(which='both', bottom=True, left=True, color=GREY)

    fig = format_bitdotio(fig, title="Labor Turnover Rates by Month, 2002-2021", text="Source: Bureau of Labor Statistics Job Openings and Labor Turnover Survey\nAccess the Data at https://bit.io/bitdotio/bls_quit_rate",
                        logo_path="../resources/logo.png", twitter_path="../resources/twitter.png")
    if show:
        plt.show()
    if save:
        if not Path("./figures/").exists():
            Path("./figures/").mkdir()
        plt.savefig("./figures/turnover_rates_fig.png")




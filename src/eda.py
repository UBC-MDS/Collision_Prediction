# author: Linh Giang Nguyen
# date: 2021-11-28

"""Creates eda plots for the pre-processed training data from the 
National Collision Database (NCDB) 2017 data (from https://open.canada.ca/data/en/
dataset/1eb9eba7-71d1-4b30-9fb1-30cbdab7e63a/resource/01426d41-529c-443f-a901-6bc2f94f3d73).
Saves the plots as png files.

Usage: src/eda.py --train=<train> --out_dir=<out_dir>

Options:
--train=<train>     Path (including filename) to training data
--out_dir=<out_dir> Path to directory where the plots should be saved
"""

from docopt import docopt
import pandas as pd
import altair as alt

alt.data_transformers.enable("data_server")
alt.renderers.enable("mimetype")

opt = docopt(__doc__)


def create_and_save_chart(df, col, save_path):
    """
    Returns distribution plots of the feature of interest from the given dataframe.
    The plot is faceted by class (no-fatality: blue, fatality: orange).

    Parameters
    ----------
    df       : str
        the given dataframe
    col      : str
        the feature of interest
    save_path :
        the path to directory where the plots should be saved

    Returns
    -------
    out: altair.vegalite.v4.api.FacetChart
       the faceted distribution plots

    Examples
    --------
    >>> create_chart(train_df, 'C_WTHR', results)
    """

    if col == "P_SEX":
        chart = (
            alt.Chart(df)
            .mark_bar(opacity=0.8)
            .encode(
                x=alt.X(col),
                y=alt.Y("count()", title="Number of collisions"),
                color=alt.Color("FATALITY", legend=None),
            )
            .properties(width=150, height=150)
            .facet("FATALITY")
            .resolve_scale(y="independent")
        )

    else:
        chart = (
            alt.Chart(df)
            .mark_bar(opacity=0.8)
            .encode(
                x=alt.X(col, type="quantitative"),
                y=alt.Y("count()", title="Number of collisions"),
                color=alt.Color("FATALITY", legend=None),
            )
            .properties(width=150, height=150)
            .facet("FATALITY")
            .resolve_scale(y="independent")
        )

    chart.save(f"{save_path}Distribution_of_{col}.png")


if __name__ == "__main__":

    train_path = opt["--train"]
    save_path = opt["--out_dir"]

    train_df = (
        pd.read_csv(train_path, low_memory=False).set_index("index").rename_axis(None)
    )

    for feature in train_df.columns:
        if feature == 'index' or feature == 'FATALITY':
            pass
        else:
            create_and_save_chart(train_df, feature, save_path)

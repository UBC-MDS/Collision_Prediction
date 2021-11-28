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

if __name__ == "__main__":

    train_path = opt["--train"]
    save_path = opt["--out_dir"]

    train_df = (
        pd.read_csv(train_path, low_memory=False).set_index("index").rename_axis(None)
    )
    
    # Converts values of P_SEX column into numeric
    sex = {'M': 1, 'F': 0, 'missing': 'missing'}
    train_df['P_SEX'] = [sex[item] for item in train_df['P_SEX']]
    
    # Creates the list of features to feed into distribution plots
    features = list(set(train_df.columns.values) - set(['index', 'FATALITY']))

    # Creates and saves distribution plots when Fatality = False
    Chart_False = (
        alt.Chart(train_df)
        .mark_bar(opacity=0.5)
        .encode(
            x=alt.X(alt.repeat("row"), type="quantitative"),
            y=alt.Y("count()", title="Number of collisions"),
            color=alt.Color("FATALITY", scale=alt.Scale(range=["blue"]), legend=None))
        .properties(width=150, height=150)
        .repeat(
            row=features,
            columns=1,
            title="FATALITY = False")
        .resolve_scale(y="independent")
        .transform_filter(alt.FieldOneOfPredicate(field="FATALITY", oneOf=[False]))
    )
    
    Chart_False.save(f"{save_path}/Distribution_of_no_fatality.png")
    
    # Creates and saves distribution plots when Fatality = True
    Chart_True = (
        alt.Chart(train_df)
        .mark_bar(opacity=0.5)
        .encode(
            x=alt.X(alt.repeat("row"), type="quantitative"),
            y=alt.Y("count()", title="Number of collisions"),
            color=alt.Color("FATALITY", scale=alt.Scale(range=["green"]), legend=None))
        .properties(width=150, height=150)
        .repeat(
            row=features,
            columns=1,
            title="FATALITY = True")
        .resolve_scale(y="independent")
        .transform_filter(alt.FieldOneOfPredicate(field="FATALITY", oneOf=[True]))
    )
    
    Chart_True.save(f"{save_path}/Distribution_of_fatality.png")




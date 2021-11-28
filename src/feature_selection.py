# author: MDS-2021-22 block3 group21
# date: 2021-11-26
"""
Imports the model pickle file and carries out Feature Selection to drop features.
Usage: feature_selection.py --input=<input filepath> --output=<output directory>

Options:
--input=<input filepath>      Filepath of the processed data
--output=<output directory>   Directory specifying where to store the model after
                              feature selection
"""

# Import libraries
import pandas as pd
from docopt import docopt

opt = docopt(__doc__)


# Feature Selection function
def main(input):

    # Import processed train data
    train_df = (
        pd.read_csv(f"{input}", low_memory=False)
        .set_index("index")
        .rename_axis(None)
    )

    # Separate train data into X_train and y_train
    X_train = train_df.drop(columns=["FATALITY"])
    y_train = train_df["FATALITY"]


if __name__ == "__main__":
    main(opt["--input"])
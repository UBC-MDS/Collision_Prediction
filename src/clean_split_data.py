# author: MDS-2021-22 block3 group21
# date: 2021-11-25
"""
Cleans NCDB 2017 data and creates training and test data set csv files.

Usage: clean_split_data.py --input=<input filepath> --output=<output directory>

Options:
--input=<input filepath>    Filepath of data in csv format
--output=<output directory> Directory specifying where to store training and test data sets
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from docopt import docopt

opt = docopt(__doc__)


def main():
    # Importing NCDB 2017 dataset
<<<<<<< HEAD
    ncdb = pd.read_csv(opt["--input"], low_memory=False, skiprows = 1).sort_index()
=======
    ncdb = pd.read_csv(opt["--input"], low_memory=False, skiprows=1).sort_index()
>>>>>>> 967de0b3b8e5d82783ca0d50d65ee4af7d55f544

    # Make all columns contain strings
    ncdb = ncdb.astype("string")

    # Create 'FATALITY' column
    ncdb.loc[ncdb["C_SEV"] == "1", "FATALITY"] = int(1)
    ncdb.loc[ncdb["C_SEV"] != "1", "FATALITY"] = int(0)

    # Dropping irrelevant or redundant columns
    ncdb = ncdb.drop(columns=["C_YEAR", "C_CASE", "P_ISEV", "V_ID", "P_ID", "C_SEV"])

    # Split data into train and test split (80:20)
    train_df, test_df = train_test_split(ncdb, test_size=0.2, random_state=21)

    # Set unknown, data not provided by jurisdiction, and "other" values to missing
    null_value = ["N", "NN", "NNNN", "Q", "QQ", "U", "UU", "UUUU", "X", "XX", "XXXX"]
    train_df = train_df.replace(to_replace=null_value, value="missing")
    test_df = test_df.replace(to_replace=null_value, value="missing")

    # Create training and test set files
    output = opt["--output"]
    train_df.to_csv(f"{output}train.csv", index_label="index")
    test_df.to_csv(f"{output}test.csv", index_label="index")
    # When reading train_df or test_df, must use .set_index("index").rename_axis(None)


if __name__ == "__main__":
    main()

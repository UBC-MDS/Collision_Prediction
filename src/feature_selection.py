# author: MDS-2021-22 block3 group21
# date: 2021-11-26
"""
Imports the model pickle file and carries out Feature Selection to drop features.
Usage: feature_selection.py --input=<input filepath> --output=<output directory>

Options:
--input=<input filepath>    Filepath of the classification model
--output=<output directory> Directory specifying where to store the model after
                            feature selection
"""

# Import libraries
import pandas as pd
import pickle

opt = docopt(__doc__)

# Feature Selection function
def main(input, output):
    # Import pickle file
    lr_model = pickle.load(open(f"{input}lr_model.rds", "rb"))


if __name__ == "__main__":
    main(opt["--input"], opt["--output"])
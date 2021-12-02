# author: DSCI-522 Group-21
# date: 2021-11-26

"""Score the model with classificaiton matrics, select the top 10 important coefficients and store the output.
Usage: scoring.py --input=<input>  --output=<output> 
 
Options:
--input=<input>       The directory where the data and model is
--output=<output>     The prefix where to write the output figure(s)/table(s) to 
"""

import os
import pandas as pd
from docopt import docopt
import pickle

import numpy as np
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, cross_validate, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix

opt = docopt(__doc__)

def main(input, output):
    # Get optimized model
    model = pickle.load(open(f"{output}final_model.rds", "rb"))
    
    # Get test data
    test_df = (
        pd.read_csv(f"{input}test.csv", low_memory=False)
        .set_index("index")
        .rename_axis(None)
    )
    X_test = test_df.drop(columns=["FATALITY"])
    y_test = test_df["FATALITY"]
    
    # Score the test data
    scores = {
        "test_score": [model.score(X_test, y_test)]
    }
    scores = pd.DataFrame(scores)
    
    # Generate the confusion matrix on test data
    conf_mat = confusion_matrix(
        y_test, 
        model.predict(X_test)
    )
    conf_mat = pd.DataFrame(conf_mat)
    
    # Save test scores
    save_df(scores, "test_scores", output)
    
    # Save confusion matrix
    save_df(conf_mat, "test_confusion_matrix", output)

# Helper function for saving dataframes
def save_df(df, name, output):
    df.to_csv(f"{output}{name}.csv")
    
    
if __name__ == "__main__":
    main(opt["--input"], opt["--output"])
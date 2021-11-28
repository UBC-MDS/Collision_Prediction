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
    
    # Get data
    train_df = (
        pd.read_csv(f"{input}train.csv", low_memory=False)
        .set_index("index")
        .rename_axis(None)
    )
    X_train = train_df.drop(columns=["FATALITY"])
    y_train = train_df["FATALITY"]
    
    test_df = (
        pd.read_csv(f"{input}test.csv", low_memory=False)
        .set_index("index")
        .rename_axis(None)
    )
    X_test = test_df.drop(columns=["FATALITY"])
    y_test = test_df["FATALITY"]
    
    # Get optimized model
    model = pickle.load(open(f"{input}final_model.rds", "rb"))
    model.fit(X_train, y_train)
    
    # Get scores
    scores = {
        "train_score": [model.score(X_train, y_train)] ,
        "test_score": [model.score(X_test, y_test)]
    }
    scores = pd.DataFrame(scores)
    
    # Get confusion matrix
    conf_mat = confusion_matrix(
        y_test, 
        model.predict(X_test)
    )
    
    # Get classification report on test data
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    class_rpt = classification_report(
        y_test, 
        y_pred, 
        target_names=["False", "True"], 
        output_dict=True
    )
    class_rpt = pd.DataFrame(class_rpt)
    
    # Save test scores
    save_df(scores, "scores", output)
    
    # Save confusion matrix
    save_df(conf_mat, "confusion_matrix", output)
    
    # Save classification report
    save_df(class_rpt, "classification_rpt", output)

# Helper funciton for saving dataframes
def save_df(df, name, output):
    df.to_pickle(f"{output}{name}.rds")
    
    
if __name__ == "__main__":
    main(opt["--input"], opt["--output"])
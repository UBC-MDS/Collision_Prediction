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
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, cross_validate
from sklearn.metrics import classification_report

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
    
    # Get cross-validation scores
    scoring = [
        "accuracy",
        "recall",
        "precision",
    ] 
    cv_scores = cross_validate(
        model, 
        X_train, 
        y_train, 
        return_train_score=True, 
        scoring = scoring
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
    
    # Get top coefficients
    random_search = pickle.load(open(f"{input}random_search.rds", "rb"))
    best_estimator = random_search.best_estimator_
    col_names = best_estimator[
        'onehotencoder'
    ].get_feature_names_out()
    weights = best_estimator["logisticregression"].coef_
    affection_coeff_df = pd.DataFrame(weights[0], index=col_names, columns=["Coefficient"])
    coeff_full = affection_coeff_df.sort_values(by="Coefficient", ascending=False)
    coeff_head = affection_coeff_df.sort_values(by="Coefficient", ascending=False).head(20)
    coeff_tail = affection_coeff_df.sort_values(by="Coefficient", ascending=False).tail(20)
    
    # Save cross-validation scores
    save_df(cv_scores, "optimized_cv_scores", output)
    
    # Save classification report
    save_df(class_rpt, "classification_rpt", output)
    
    # Save coefficient tables
    save_df(coeff_full, "coeff_fulls", output)
    save_df(coeff_head, "coeff_head", output)
    save_df(coeff_tail, "coeff_tail", output)
    
# Helper funciton for saving dataframes
def save_df(df, name, output):
    df.to_pickle(f"{output}{name}.rds")
    
    
if __name__ == "__main__":
    main(opt["--input"], opt["--output"])
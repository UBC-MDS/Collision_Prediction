# author: Siqi Tao
# date: 2021-11-26

"""Perform machine learning analysis on the cleaned data
Usage: model.py --input=<input>  --output=<output> 
 
Options:
--input=<input>       The path or filename pointing to the data
--output=<output>     The prefix where to write the output figure(s)/table(s) to and what to call it 
"""

import os
import pandas as pd
from docopt import docopt

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer
from sklearn.model_selection import (
    RandomizedSearchCV,
    cross_val_score,
    cross_validate
)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder
from scipy.stats import loguniform
from sklearn.metrics import confusion_matrix
import pickle

opt = docopt(__doc__)

def main(): 
    
    # Get data
    input = opt["--input"]
    train_df = pd.read_csv(f"{input}train.csv", low_memory=False)
    test_df = pd.read_csv(f"{input}test.csv", low_memory=False)
    
    X_train = train_df.drop(columns=["FATALITY"])
    X_test = test_df.drop(columns=["FATALITY"])
    
    y_train = train_df["FATALITY"]
    y_test = test_df["FATALITY"]
    
    # Convert columns into string data type
    cols = X_train.columns.tolist()
    for i in range(len(cols)):
        X_train[cols[i]] = X_train[cols[i]].astype(str)
        X_test[cols[i]] = X_test[cols[i]].astype(str)
    
    #Transform columns (all categorical)
    categorical_feats = cols
    preprocessor = make_column_transformer(
        (OneHotEncoder(handle_unknown="ignore", sparse=False), categorical_feats),
    )
    
    preprocessor.fit(X_train)
    
    # Get column names
    columns = list(
        preprocessor.named_transformers_["onehotencoder"].get_feature_names_out(
            categorical_features
        )
    )
    
    # Pipeline including OneHotEncoder and LogisticRegression
    pipe = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False), 
        LogisticRegression(max_iter=2000)
    )
    
    # Scoring include accuracy, f1, recall, precision. 
    results = {}
    scoring = [
        "accuracy",
        "f1", 
        "recall", 
        "precision", 
        "roc_auc", 
        "average_precision"
    ]
    results["Logistic Regression"] = mean_std_cross_val_scores(pipe, X_train, y_train, scoring=scoring)
    result_df = pd.DataFrame(results)
    
    # Plot confusion matrix
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_train)
    conf_mat = confusion_matrix(y_train, preds)
    conf_mat = pd.DataFrame(conf_mat)
    
    # Hyperparameter tuning using RandomSearchCV 
    # Optimize using f1 as we have class imbalance.
    param_grid = {
        "logisticregression__C": loguniform(1e-3, 1e3),
        "logisticregression__class_weight": [None, "balanced"],
    }
    random_search = RandomizedSearchCV(
        pipe,
        param_grid,
        n_iter=50,
        verbose=1,
        n_jobs=-1,
        random_state=123,
        return_train_score=True,
        scoring="f1"
    )
    random_search.fit(X_train, y_train)
    print("Best hyperparameter values: ", random_search.best_params_)
    print("Best score: %0.3f" % (random_search.best_score_))
    
    # Create output tables/images
    output = opt["--output"]
    save_df(result_df, "score_results")
    save_df(conf_mat, "confusion matrix")
    
    # Storing optimized model
    pickle.dump(model, open(f"{input}final_model.rds", "wb"))
    
# Function obtained from DSCI-571 lecture notes
def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):
    """
    Returns mean and std of cross validation

    Parameters
    ----------
    model :
        scikit-learn model
    X_train : numpy array or pandas DataFrame
        X in the training data
    y_train :
        y in the training data

    Returns
    ----------
        pandas Series with mean scores from cross_validation
    """

    scores = cross_validate(model, X_train, y_train, **kwargs)

    mean_scores = pd.DataFrame(scores).mean()
    std_scores = pd.DataFrame(scores).std()
    out_col = []

    for i in range(len(mean_scores)):
        out_col.append((f"%0.3f (+/- %0.3f)" % (mean_scores[i], std_scores[i])))

    return pd.Series(data=out_col, index=mean_scores.index)
    
def save_df(df, name):
    df.to_pickle(f"{output}{name}.rds")    
    
if __name__ == "__main__":
    main() 
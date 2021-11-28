# author: DSCI-522 Group-21
# date: 2021-11-26

"""Perform machine learning analysis on the cleaned data
Usage: model.py --input=<input>  --output=<output> 
 
Options:
--input=<input>       The path or filename pointing to the data
--output=<output>     The prefix where to write the output figure(s)/table(s) to
"""

import os
import pandas as pd
from docopt import docopt

import numpy as np
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, cross_validate
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder
from scipy.stats import loguniform
from sklearn.metrics import confusion_matrix
import pickle
import imblearn
from imblearn.pipeline import make_pipeline as make_imb_pipeline
from imblearn.under_sampling import RandomUnderSampler

opt = docopt(__doc__)

def main(input, output):

    # Get data
    train_df = (
        pd.read_csv(f"{input}", low_memory=False)
        .set_index("index")
        .rename_axis(None)
    )
    X_train = train_df.drop(columns=["FATALITY"])
    y_train = train_df["FATALITY"]

    # Convert columns into string data type
    cols = X_train.columns.tolist()
    for i in range(len(cols)):
        X_train[cols[i]] = X_train[cols[i]].astype(str)

    # Pipeline including RandomUnderSampler, OneHotEncoder, and LogisticRegression
    # Using undersampling to address class imbalance
    pipe = make_imb_pipeline(
        RandomUnderSampler(random_state=21),
        OneHotEncoder(handle_unknown="ignore", sparse=False),
        LogisticRegression(max_iter=2000)
    )

    # Determine cross-validation accuracy of unoptimized model
    # Only need accuracy as classes are now balanced
    results = {}
    results["Logistic Regression"] = mean_std_cross_val_scores(
        pipe, X_train, y_train, return_train_score=True
    )

    # Hyperparameter tuning using RandomSearchCV
    param_grid = {
        "logisticregression__C": loguniform(1e-3, 1e3),
    }
    random_search = RandomizedSearchCV(
        pipe,
        param_grid,
        n_iter=50,
        verbose=1,
        n_jobs=-1,
        random_state=123,
        return_train_score=True
    )
    random_search.fit(X_train, y_train)
    print("Best hyperparameter values: ", random_search.best_params_)
    print("Best score: %0.3f" % (random_search.best_score_))

    # Create optimized model
    imb_pipeline = make_imb_pipeline(
        RandomUnderSampler(random_state=21),
        OneHotEncoder(handle_unknown="ignore", sparse=False),
        LogisticRegression(
            max_iter=2000,
            C=random_search.best_params_["logisticregression__C"]
        )
    )

    # Determine cross-validation scores of optimized model
    results["Logistic Regression Optimized"] = mean_std_cross_val_scores(
        imb_pipeline, X_train, y_train, return_train_score=True
    )
    result_df = pd.DataFrame(results)
    result_df.index.name = "score_type"

    # Create output tables/images
    result_df.to_csv("results/score_results.csv")

    # Creating the best model
    model = LogisticRegression(
        max_iter=2000,
        C=random_search.best_params_["logisticregression__C"]
    )

    # Storing logistic regression model
    pickle.dump(model, open(f"{output}lr_model.rds", "wb"))


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


if __name__ == "__main__":
    main(opt["--input"], opt["--output"])

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
import pickle
from imblearn.pipeline import make_pipeline as make_imb_pipeline
from imblearn.under_sampling import RandomUnderSampler
from sklearn.feature_selection import RFECV
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import get_scorer, confusion_matrix

opt = docopt(__doc__)


# Feature Selection function
def main(input, output):

    # Import processed train data
    train_df = (
        pd.read_csv(f"{input}", low_memory=False)
        .set_index("index")
        .rename_axis(None)
    )

    # Separate train data into X_train and y_train
    X_train = train_df.drop(columns=["FATALITY"])
    y_train = train_df["FATALITY"]

    # Import pickle file
    lr_model = pickle.load(open(f"{output}lr_model.rds", "rb"))

    # Feature Selection using RandomUnderSampler, OneHotEncoder, RFECV,
    # and Logistic Regression model with best parameters
    pipe_ohe_rfe_lr = make_imb_pipeline(
        RandomUnderSampler(random_state=21),
        OneHotEncoder(handle_unknown="ignore"),
        RFECV(lr_model, cv=5),
        lr_model
    )

    # Fitting the pipeline
    final_model = pipe_ohe_rfe_lr.fit(X_train, y_train)

    # Saving final model
    pickle.dump(final_model, open(f"{output}final_model.rds", "wb"))

    # Generating scores on the updated LR model
    score_dict = {}
    scoring_metrics = ['accuracy', 'f1', 'precision', 'recall']

    score_dict['LR after Feature Selection'] = {
        scorer: get_scorer(scorer)(pipe_ohe_rfe_lr, X_train, y_train) for scorer in scoring_metrics
    }

    scores = pd.DataFrame(score_dict)
    scores.index.name = "scoring_metric"

    # Save scores table
    save_df(scores, "scores_after_FS", output)

    # Generate the confusion matrix
    conf_mat = confusion_matrix(
        y_train, 
        final_model.predict(X_train),
        labels=[False, True]
    )
    conf_mat = pd.DataFrame(conf_mat, columns=["non_fatal", "fatal"])
    conf_mat = conf_mat.assign(actuals=["non_fatal", "fatal"])
    conf_mat = conf_mat.set_index('actuals')

    # Save confusion matrix
    save_df(conf_mat, "train_confusion_matrix", output)

    # Print model accuracy
    print("Model accuracy after feature selection:", scores.iloc[0, 0])

# Helper function for saving dataframes
def save_df(df, name, output):
    df.to_csv(f"{output}{name}.csv")

if __name__ == "__main__":
    main(opt["--input"], opt["--output"])
# author: DSCI-522 Group-21
# date: 2021-11-26

"""Score the model with the test set and generate a confusion matrix
Usage: scoring.py --input=<input>  --output=<output> 
 
Options:
--input=<input>       The directory where the data and model is
--output=<output>     Directory specifying where to store output figure(s)/table(s)
"""

import pandas as pd
from docopt import docopt
import pickle
from sklearn.metrics import confusion_matrix, get_scorer

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

    # Check if the required columns exists in the test file
    assert set(test_df.columns) == {
        "C_MNTH",
        "C_WDAY",
        "C_HOUR",
        "C_VEHS",
        "C_CONF",
        "C_RCFG",
        "C_WTHR",
        "C_RSUR",
        "C_RALN",
        "C_TRAF",
        "V_TYPE",
        "V_YEAR",
        "P_SEX",
        "P_AGE",
        "P_PSN",
        "P_SAFE",
        "P_USER",
        "FATALITY"
    }, "Required Columns not found in input .csv file"

    X_test = test_df.drop(columns=["FATALITY"])
    y_test = test_df["FATALITY"]
    
    # Import training scores df
    results_df = (
        pd.read_csv(f"{output}final_training_scores.csv", index_col=0)
    )

    # Create list of desired scoring metrics
    scoring_metrics = ["accuracy", "f1", "recall", "precision", "average_precision"]

    # Score the test data
    scores = {
    scorer: [
        round(get_scorer(scorer)(model, X_test, y_test), 3)
        ] for scorer in scoring_metrics
    }

    scores = pd.DataFrame(scores, index=["test_scores"])

    final_results = results_df.append(scores)
    final_results = final_results.rename_axis("score")
    
    # Save test scores with training scores
    save_df(final_results, "final_scores", output)

    # Generate the confusion matrix on test data
    conf_mat = confusion_matrix(
        y_test, 
        model.predict(X_test)
    )
    conf_mat = pd.DataFrame(conf_mat, columns=["non_fatal", "fatal"])
    conf_mat = conf_mat.assign(actuals=["non_fatal", "fatal"])
    conf_mat = conf_mat.set_index('actuals')
    
    # Save confusion matrix
    save_df(conf_mat, "test_confusion_matrix", output)

# Helper function for saving dataframes
def save_df(df, name, output):
    df.to_csv(f"{output}{name}.csv")
    
    
if __name__ == "__main__":
    main(opt["--input"], opt["--output"])
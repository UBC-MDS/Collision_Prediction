Collision Prediction Report
================
Abdul Moid Mohammed
24/11/2021

-   [The Question](#the-question)
-   [The Analysis](#the-analysis)
-   [The Results](#the-results)
-   [The Findings](#the-findings)
-   [The Critique](#the-critique)
-   [Including Plots](#including-plots)

## The Question

Stemming from the daily news we come across on fatalities due to motor
vehicle collisions, we wanted to design a model that would help predict
whether a motor vehicle collision would result in a fatality or not,
which lead to our predictive research question: “Will a motor vehicle
collision result in fatalities?”. But would it suffice to only “predict”
a fatality? How about determining some of the major contributors that
could result in a fatal collision? Through this predictive analysis we
first aim to predict whether a collision would result in a fatality or
not followed by determining what features are most important in making
these predictions. Specifically, we want to know how important weather,
road type, time of year, age of driver, and vehicle type are in
predicting the severity of a motor vehicle collision.

This is an R Markdown document. Markdown is a simple formatting syntax
for authoring HTML, PDF, and MS Word documents. For more details on
using R Markdown see <http://rmarkdown.rstudio.com>.

When you click the **Knit** button a document will be generated that
includes both content as well as the output of any embedded R code
chunks within the document. You can embed an R code chunk like this:

``` r
summary(cars)
```

    ##      speed           dist       
    ##  Min.   : 4.0   Min.   :  2.00  
    ##  1st Qu.:12.0   1st Qu.: 26.00  
    ##  Median :15.0   Median : 36.00  
    ##  Mean   :15.4   Mean   : 42.98  
    ##  3rd Qu.:19.0   3rd Qu.: 56.00  
    ##  Max.   :25.0   Max.   :120.00

## Model
The Logistic Regression algorithm was used to build a classification model to predict whether a motor vehicle collision leads to a fatality or not. All variables included in the original data set, with the exception of “C_YEAR”, “C_CASE”, “C_SEV”, “P_ISEV”, “V_ID”, and “P_ID” were used to fit the model, as these features were either irrelevant to our prediction or contained redundant information. The “FATALITY” column was created using the “P_ISEV” by converting values that correspond to a fatality as “True”, and converting values that correspond to an injury or no injury as “False”. The “FATALITY” column served as the target column to be predicted. In order to tackle the issue of class imbalance and to perform cross-validations in feasible times with our available computing power, we performed random undersampling using RandomUnderSampler. Since all features were categorical, our pipeline consisted of the RandomUnderSampler, a OneHotEncoder, and the LogisticRegression model. We determined the optimal value of the logistic regression model’s hyperparameter, $C$, using 5-fold cross validation with random search RandomizedSearchCV. We further performed feature selection using RandomUnderSampler, OneHotEncoder, RFECV, and LogisticRegression model to reduce the number of features. The R and Python programming languages [@R; @Python] and the following R and Python packages were used to perform the analysis: knitr [@knitr], docopt [@docoptpython], os [@Python], Pandas [@mckinney-proc-scipy-2010], scikit-learn [@scikit-learn], imbalance-learn [@Imbalance-learn], Altair [@altair], Vegalite [@vegalite]. The code used to perform the analysis and create this report can be found here: https://github.com/UBC-MDS/Collision_Prediction.


## The Results

Once we identify the important features through EDA, we will proceed
with preprocessing the data by applying the relevant transformations. We
will then subject the preprocessed data to different classification
models such as decision trees, k-NN, RBF SVC, Naive Bayes, and Logistic
Regressors. Then cross-validation and hyperparameter optimization will
be performed to determine the model with the best
hyperparameters/scores. We will move forward with the best
classification model to answer our research question.

## The Findings

The best model will then be fitted on the entire training set and
evaluated with the test set. The results of our analyses will be
presented as a table of classification scoring metrics obtained from the
test set, to show how well our model performs and how well it
generalizes to new data.

## The Critique

#### Limitations

Some of the limitations of the c

#### Assumptions

We have assumed that:

Logistic Regression is the best model to make predictions ## Future
Directions In future, we would like to improvise the analysis by trying
out various classification models to do a comparative study and
determine the best classification model. Some of the other models that
we are interested in are: Decision Tree Classifier, k-NN Classifier, RBF
SVC, Naive Bayes.

## Including Plots

You can also embed plots, for example:

![](collision_prediction_report_files/figure-gfm/pressure-1.png)<!-- -->

Note that the `echo = FALSE` parameter was added to the code chunk to
prevent printing of the R code that generated the plot.

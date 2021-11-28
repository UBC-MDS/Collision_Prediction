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

## The Analysis

With the research question in mind, we begin our analysis by first
separating the data into a training set and test set (split 90:10). On
the training set we will perform EDA to assess the presence or absence
of class imbalance, determine what sort of preprocessing is required,
and to discern which features may be most important for prediction. The
class imbalance will be assessed by presenting the class counts as a
table. To determine the necessary preprocessing transformations, we will
include a pandas.DataFrame.info table which presents the data types and
amount of missing values. Additionally, we will include a
pandas.DataFrame.describe table to obtain informative descriptive
statistics such as the central tendency, spread, and shape of the
training set. To discern important features for prediction we will plot
histograms presenting the distribution of each numeric feature in the
dataset facetted on the target classes in our EDA.

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

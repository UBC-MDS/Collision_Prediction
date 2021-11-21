# Fatality of Canadian Motor Vehicle Collisions Predictor

## Project Proposal

The data set that will be used in this project came from the National Collision Database published by Transport Canada and can be found [here](https://open.canada.ca/data/en/dataset/1eb9eba7-71d1-4b30-9fb1-30cbdab7e63a). The National Collision Database contains data on all of the police-reported motor vehicle collisions on public roads in Canada from 1999 to the most recent available data from 2017. This data set contains information licensed under the Open Government Licence – Canada.

In this project we want to answer the research question, "Will a motor vehicle collision in Canada result in fatalities?"

Related sub-questions of interest are, "What features best predict a severe motor vehicle collision?" Where severe is defined as a collision involving fatalities. Specifically, we want to know how important weather, road type, time of year, age of driver, and vehicle type are in predicting the severity of a motor vehicle collision.

After preprocessing the data, we aim to try different classification models such as decision trees, kNN, RBF SVC, Naive Bayes, and logistic regressors. After tuning hyperparameters and determining which model is likely to perform the best on the test data, we will move forward with that model as the classifier we will use to answer the research question.

To determine the data types and amount of null values present in our data set we will include a `pandas.DataFrame.info table` in our EDA. To obtain descriptive statistics such as the central tendency, spread, and shape of the data set we will include a `pandas.DataFrame.describe` table. To visualize how the distributions of the features change with respect to target class, we will include histograms presenting the distribution of each numeric feature in the dataset facetted on the target classes in our EDA.

The results of our analyses would be presented as a table of classification scoring metrics obtained from the test set, to show how well our model performs and how well it generalizes to new data.
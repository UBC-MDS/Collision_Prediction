# Motor Vehicle Collision Fatality Predictor

* Authors: Abdul Moid Mohammed, Daniel King, Doris Tao, Linh Giang Nguyen

## About

In this project we build a classification model to attempt to answer the predictive research question, "Will a motor vehicle collision result in fatalities?" EXPLAIN RESULTS

The data set that was used in this project came from the National Collision Database, published by Transport Canada, which can be found [here](https://open.canada.ca/data/en/dataset/1eb9eba7-71d1-4b30-9fb1-30cbdab7e63a). The National Collision Database contains data on all of the police-reported motor vehicle collisions on public roads in Canada from 1999 to the most recent available data from 2017. We ran our analysis using the data collected from collisions that occurred in 2017. This data set contains information licensed under the Open Government Licence – Canada.

## Report

The final report can be found [here]("")

## Usage

To replicate this analysis, clone this GitHub repository, install the listed [dependencies](#Dependencies), and run the following commands from the terminal/command line from within the project's root directory:

```
# download data
python src/download_data.py --url="https://opendatatc.blob.core.windows.net/opendatatc/NCDB_2017.csv" --filepath=data/raw/NCDB_2017.csv

# clean and split data
python src/clean_split_data.py --input=data/raw/NCDB_2017.csv --output=data/processed/

# run eda report
python src/eda.py --train=data/processed/NCDB_2017.csv --out_dir=results/figures/

# create and tune model
python src/model.py --input=data/processed/train.csv --output=results/

# select features

# test model

# render final report

```

## Dependencies

* Python 3.10.0 and Python packages:
  * altair=4.1.0=py_1
  * altair_saver
  * imbalanced-learn
  * pandas==1.3.4
  * scikit-learn==1.0.1
  * docopt-ng==0.7.2

## License

The Motor Vehicle Collision Fatality Predictor materials here are licensed under the MIT License. If you use or re-mix this project please provide attribution and a link to this GitHub repository.
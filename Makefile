# collision prediction pipe
# author: MDS-2021-22 block3 group21
# date: 2021-11-30

# download data
#data/raw/NCDB_2017.csv : src/download_data.py
#	python src/download_data.py --url=https://opendatatc.blob.core.windows.net/opendatatc/NCDB_2017.csv --filepath=data/raw/NCDB_2017.csv

# clean and split data 
data/processed/train.csv data/processed/test.csv : src/clean_split_data.py data/raw/NCDB_2017.csv
	python src/clean_split_data.py --input=data/raw/NCDB_2017.csv --output=data/processed/

# run eda report
results/Distribution_of_no_fatality.png results/Distribution_of_fatality.png : src/eda.py data/processed/train.csv
	python src/eda.py --train=data/processed/train.csv --out_dir=results/

# create and tune model
results/lr_model.rds results/score_results.csv : src/model.py data/processed/train.csv
	python src/model.py --input=data/processed/train.csv --output=results/
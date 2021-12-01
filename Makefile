# collision prediction pipe
# author: MDS-2021-22 block3 group21
# date: 2021-11-30

# download data
#data/raw/NCDB_2017.csv : src/download_data.py
#	python src/download_data.py --url=https://opendatatc.blob.core.windows.net/opendatatc/NCDB_2017.csv --filepath=data/raw/NCDB_2017.csv

# clean and split data 
data/processed/train.csv data/processed/test.csv : src/clean_split_data.py data/raw/NCDB_2017.csv
	python src/clean_split_data.py --input=data/raw/NCDB_2017.csv --output=data/processed/
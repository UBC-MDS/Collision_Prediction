# collision prediction pipe
# author: MDS-2021-22 block3 group21
# date: 2021-11-30

# all
all : doc/collision_prediction_report.md

# download data
data/raw/NCDB_2017.csv : src/download_data.py
	python src/download_data.py --url="https://raw.githubusercontent.com/UBC-MDS/National_Collision_DB_Group407/master/data/raw_data.csv" --filepath=data/raw/NCDB_2017.csv

# clean and split data 
data/processed/train.csv data/processed/test.csv : src/clean_split_data.py data/raw/NCDB_2017.csv
	python src/clean_split_data.py --input=data/raw/NCDB_2017.csv --output=data/processed/

# run eda report
results/Distribution_of_no_fatality.png results/Distribution_of_fatality.png : src/eda.py data/processed/train.csv
	python src/eda.py --train=data/processed/train.csv --out_dir=results/

# create and tune model
results/lr_model.rds results/CV_results.csv : src/model.py data/processed/train.csv
	python src/model.py --input=data/processed/train.csv --output=results/

# feature selection
results/final_model.rds results/final_training_scores.csv : src/feature_selection.py data/processed/train.csv results/lr_model.rds
	python src/feature_selection.py --input=data/processed/train.csv --output=results/

# score test data
results/final_scores.csv results/test_confusion_matrix.csv : src/score.py data/processed/test.csv results/final_model.rds results/final_training_scores.csv
	python src/score.py --input=data/processed/ --output=results/

# render final report
doc/collision_prediction_report.md : doc/collision_prediction_report.Rmd doc/collision_prediction_references.bib results/Distribution_of_no_fatality.png results/Distribution_of_fatality.png results/CV_results.csv results/final_scores.csv results/test_confusion_matrix.csv
	Rscript -e "rmarkdown::render('doc/collision_prediction_report.Rmd')"

# clean
clean :
	rm -rf data/raw/NCDB_2017.csv
	rm -rf data/processed/train.csv
	rm -rf data/processed/test.csv
	rm -rf results/*.png
	rm -rf results/*.rds
	rm -rf results/*.csv
	rm -rf doc/collision_prediction_report.md
	rm -rf doc/*.pdf
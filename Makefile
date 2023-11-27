.PHONY: build run

build:
	python3 -m build

run:
	#python3 src/analysis/main.py --pdfs-folder src/data_0611/
	python3 main.py './test_data' './predictions.csv'


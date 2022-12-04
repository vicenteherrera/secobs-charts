

.PHONY: all
all: install download_charts_info evaluate postprocess

.PHONY: download_charts_info
download_charts_info:
	helm search hub -o yaml > result/charts_ah_source.yaml

.PHONY: install
install:
	poetry install

.PHONY: evaluate
evaluate:
	mkdir -p ./result/cache
	poetry run python3 src/charts_eval/main.py evaluate

.PHONY: postprocess
postprocess:
	mkdir -p ./result/docs
	poetry run python3 src/charts_eval/main.py postprocess

# Reset --------------------------------------------------------

reset-cache:
	rm result/cache/* ||:

reset-db:
	rm result/charts_db.yaml ||:

full-reset: reset-db reset-cache
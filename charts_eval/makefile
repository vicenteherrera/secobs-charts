

.PHONY: all
all: install download_charts_info evaluate postprocess

.PHONY: prerequisites
prerequisites:
	jq --version
	yq version
	helm version

.PHONY: install
install:
	poetry install
	mkdir -p ./result/cache
	mkdir -p ./result/docs

.PHONY: download_charts_info
download_charts_info:
	helm search hub -o yaml > result/charts_ah_source.yaml

.PHONY: evaluate
evaluate:
	poetry run python3 src/charts_eval/main.py evaluate

.PHONY: postprocess
postprocess:
	poetry run python3 src/charts_eval/main.py postprocess

# Reset --------------------------------------------------------

.PHONY: reset-cache
reset-cache:
	rm result/cache/* ||:

.PHONY: reset-db
reset-db:
	rm result/charts_db.yaml ||:

.PHONY: full-reset
full-reset: reset-db reset-cache

# Commit docs ---------------------------------------------------

.PHONY: push-gen-docs
push-gen-docs:
	git pull
	git add ../docs/generated/*
	git commit -m "Updated generated docs chart evaluation $(shell date +'%Y-%m-%d %H:%M:%S')"
	git push

.PHONY: all
all: install download_charts_info generate evaluate postprocess push

# Preparation --------------------------------------------------------

.PHONY: prerequisites
prerequisites:
	jq --version
	yq version
	helm version

.PHONY: install
install:
	curl -fsSL https://raw.githubusercontent.com/vicenteherrera/psa-checker/main/install/install.sh | INSTALL_DIR=$(shell go env GOPATH)/bin bash
	poetry install
	mkdir -p ./result/cache

# Execution --------------------------------------------------------

.PHONY: download_charts_info
download_charts_info:
	helm search hub -o yaml > result/charts_ah_source.yaml

.PHONY: generate
generate:
	poetry run python3 src/charts_eval/main.py generate

.PHONY: evaluate
evaluate:
	poetry run python3 src/charts_eval/main.py evaluate

.PHONY: evaluate_force
evaluate_force:
	poetry run python3 src/charts_eval/main.py evaluate --force

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

.PHONY: push
push:
	git pull
	git add ../docs/generated/*
	git commit -m "Updated generated docs chart evaluation $(shell date +'%Y-%m-%d %H:%M:%S')"
	git push

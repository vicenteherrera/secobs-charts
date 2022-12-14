
.PHONY: all
all: install prerequisites download-charts-source generate evaluate postprocess

# Preparation --------------------------------------------------------

.PHONY: prerequisites
prerequisites:
	jq --version
	yq --version
	helm version
	psa-checker version
	badrobot version
	poetry --version


.PHONY: install
install:
	curl -fsSL https://raw.githubusercontent.com/vicenteherrera/psa-checker/main/install/install.sh | INSTALL_DIR=$(shell go env GOPATH)/bin bash
	go install github.com/controlplaneio/badrobot@latest
	poetry install
	mkdir -p ./result/cache

# Execution --------------------------------------------------------

.PHONY: download-charts-source
download-charts-source:
	helm search hub -o yaml > result/charts_ah_source.yaml

.PHONY: generate
generate:
	poetry run python3 src/charts_eval/main.py generate

.PHONY: generate
generate-retry-errors:
	poetry run python3 src/charts_eval/main.py generate --retry-errors

.PHONY: evaluate
evaluate:
	poetry run python3 src/charts_eval/main.py evaluate

.PHONY: evaluate-force
evaluate-force:
	poetry run python3 src/charts_eval/main.py evaluate --force

.PHONY: postprocess
postprocess:
	poetry run python3 src/charts_eval/main.py postprocess

# Reset --------------------------------------------------------

.PHONY: reset-cache
reset-cache:
	@rm -r ./result/cache/ 2>/dev/null ||:
	@mkdir -p ./result/cache/

.PHONY: reset-db
reset-db:
	@rm ./result/charts_db.yaml 2>/dev/null ||:

.PHONY: reset-full
reset-full: reset-db reset-cache
	rm -r $$HOME/.cache/helm/repository ||:
	rm -r $$HOME/.helm/repository ||:
	mkdir -p $$HOME/.cache/helm/repository
	mkdir -p $$HOME/.helm/repository

# Test --------------------------------------------------------

.PHONY: test-e2e
test-e2e: reset-full
	cp ./tests/charts_ah_source.yaml ./result


# Download from live server -------------------------------------

.PHONY: download-result
download-result:
	rm -r ./result ||:
	mkdir -p ./result
	echo "Downloading results from online server"
	ssh $$ONLINEHOST "cd $$ONLINEPATH;tar zc result" | tar zx

# Commit docs ---------------------------------------------------

.PHONY: push
push:
	git pull
	git add ../docs/generated/*
	git commit -m "Updated generated docs chart evaluation $(shell date +'%Y-%m-%d %H:%M:%S')"
	git push

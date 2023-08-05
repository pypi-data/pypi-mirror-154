.PHONY: help
help: ## show help
	@grep -h '##\ [[:alnum:]]' $(MAKEFILE_LIST) | sed -E 's/(.*):.*##(.*)/\1: \2/' | column -s: -t

venv: ## create venv
	python3 -m venv venv

.PHONY: install
install: venv ## install/upgrade packaging tools
	venv/bin/pip install --upgrade --upgrade-strategy eager build pip tox twine

.PHONY: develop
develop: install ## install package in 'development mode'
	venv/bin/python -m pip install -e .

.PHONY: test
test: install ## run tests
	venv/bin/tox

.PHONY: clean
clean: ## cleanup
	@echo "Cleaning up distutils stuff"
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info/
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
	find . -type d -name "__pycache__" -delete
	@echo "Cleaning up test stuff"
	rm -rf .pytest_cache
	rm -rf .tox

.PHONY: build
build: clean ## build
	venv/bin/python -m build

.PHONY: upload_test
upload_test: build ## upload to https://test.pypi.org
	venv/bin/twine upload --repository testpypi dist/*

.PHONY: upload
upload: build ## upload to https://pypi.org
	venv/bin/twine upload dist/*

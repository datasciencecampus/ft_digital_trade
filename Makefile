.PHONY:
	coverage
	coverage_html
	coverage_xml
	docs
	docs_check_external_links
	help
	prepare_docs_folder
	requirements
	create_venv
	create_kernel
	venv
	delete_venv

.DEFAULT_GOAL := help

## Install the Python requirements for contributors, and install pre-commit hooks
pre_commit:
	python -m pip install -U pip setuptools
	python -m pip install pre-commit
	pre-commit install

## Install a venv

# Define the name of the virtual environment based on the current directory
VENV_NAME = venv_$(shell basename $(CURDIR))

# Target to create a virtual environment and install requirements.txt
create_venv:
	python -m venv $(VENV_NAME)
	bash -c "source $(VENV_NAME)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

# Target to create an IPython kernel
create_kernel: create_venv
	bash -c 'source $(VENV_NAME)/bin/activate && pip install ipykernel && python -m ipykernel install --user --name $(VENV_NAME) --display-name "Python - $(VENV_NAME)"'

# Target to set up the environment (create venv, install requirements, and create kernel)
venv: create_kernel

# Target to delete the virtual environment and IPython kernel
delete_venv:
	# Remove the virtual environment directory
	rm -rf $(VENV_NAME)
	# Remove the IPython kernel
	jupyter kernelspec remove -f $(VENV_NAME)

## Create a `docs/_build` folder, if it does not exist. Otherwise delete any sub-folders and their contents within it
prepare_docs_folder:
	if [ ! -d "./docs/_build" ]; then mkdir ./docs/_build; fi
	find ./docs/_build -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} \;

## Compile the Sphinx documentation in HTML format in the docs/_build folder from a clean build
docs: prepare_docs_folder requirements
	sphinx-build -b html ./docs ./docs/_build

## Check external links in the Sphinx documentation using linkcheck in the docs/_build folder from a clean build
docs_check_external_links: prepare_docs_folder requirements
	sphinx-build -b linkcheck ./docs ./docs/_build

## Run code coverage
coverage: requirements
	coverage run -m pytest

## Run code coverage, and produce a HTML output
coverage_html: coverage
	coverage html

## Run code coverage, and produce an XML output
coverage_xml: coverage
	coverage xml

## Get help on all make commands; referenced from https://github.com/drivendata/cookiecutter-data-science
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=25 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')

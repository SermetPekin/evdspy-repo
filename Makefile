# Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
TEST_DIR = tests

# Targets
all: install test

.PHONY: venv
venv:
	python3 -m venv $(VENV)

.PHONY: install
install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

.PHONY: test
test:
	python3.11 -m pip install -r ./requirements-dev.txt
	pytest -v 
	tox run 
.PHONY: lint
lint:
	$(PYTHON) -m flake8 .

.PHONY: format
format:
	$(PYTHON) -m black .

.PHONY: check
check:
	ruff check 
	tox run 

.PHONY: security
security:
	python3.11 -m pip install safety
	python3.11 -m safety check --ignore=70612



clean:
	rm -rf $(VENV)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: help
help:
	@echo "Makefile targets:"
	@echo "  venv       - Create a virtual environment"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  lint       - Lint the code"
	@echo "  format     - Format the code"
	@echo "  clean      - Clean up the environment"

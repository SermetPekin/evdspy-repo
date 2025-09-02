# Variables
VENV = venv
PYTHON = $(VENV)
TEST_DIR = tests

# Targets
all: install test

.PHONY: venv
venv:
	python -m venv $(VENV)

.PHONY: install
install: venv
	$(VENV)/Scripts/python -m pip install --upgrade pip
	$(VENV)/Scripts/python -m pip install -r requirements.txt

.PHONY: test
test:
	python -m pip install -r requirements-dev.txt
	pytest -v
	tox
.PHONY: lint
lint:
	python -m flake8 .

.PHONY: format
format:
	python -m black .

.PHONY: check
check:
	ruff check
	tox

.PHONY: security
security:
	python -m pip install safety
	python -m safety check --ignore=70612



clean:
	python -c "import shutil; shutil.rmtree('$(VENV)', ignore_errors=True)"
	python -c "import os; [os.remove(f) for d,_,fs in os.walk('.') for f in [os.path.join(d,ff) for ff in fs if ff.endswith('.pyc')]]"
	python -c "import os; [shutil.rmtree(os.path.join(d,'__pycache__'), ignore_errors=True) for d,dirs,fs in os.walk('.') if '__pycache__' in dirs]"

.PHONY: help
help:
	@echo "Makefile targets:"
	@echo "  venv       - Create a virtual environment"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  lint       - Lint the code"
	@echo "  format     - Format the code"
	@echo "  clean      - Clean up the environment"

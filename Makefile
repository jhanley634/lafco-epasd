
#
ENV_DIR = $(HOME)/.venv/lafco-epasd
ACTIVATE = source $(ENV_DIR)/bin/activate

all: $(ENV_DIR)

venv: $(ENV_DIR)
$(ENV_DIR):
	python --version && echo
	python -c 'import sys; print("\n", sys.version_info, "\n")'
	@# Please use cPython 3.12 or higher.
	python -c 'import sys; assert sys.version_info >= (3, 12)'
	mkdir -p $(ENV_DIR)
	python -m venv $(ENV_DIR)

install: $(ENV_DIR)
	$(ACTIVATE) && pip install -r requirements.txt
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && bin/version_audit.py

STRICT ?= --strict --warn-unreachable --ignore-missing-imports --no-namespace-packages
lint:
	$(ACTIVATE) && black . && isort . && ruff check
	$(ACTIVATE) && mypy $(STRICT) .

.PHONY: install venv

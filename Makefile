VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

activate:
	@echo "Run:"
	@echo "source $(VENV)/bin/activate"

norm:
	$(PYTHON) -m flake8 *.py

deactivate:
	@echo "Run:"
	@echo "deactivate"

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pkl" -delete
	find . -type f -name "*.pdf" -delete

.PHONY: clean, activate, deactivate, setup, norm

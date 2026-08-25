VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

help:
	@echo "To run learn2slither manually:"
	@echo "python3 slither_main.py"
	@echo "Options:"
	@echo "--sessions : number of sessions"
	@echo "--load : name of model to load"
	@echo "--save : filename to save model to"
	@echo "--display : (on/off) display graphics"
	@echo "--step : (yes/no) step-by-step snake display"
	@echo "--explore : (yes/no) yes for training, no for exploitation"

activate:
	@echo "Run:"
	@echo "source $(VENV)/bin/activate"

norm:
	$(PYTHON) -m flake8 *.py

deactivate:
	@echo "Run:"
	@echo "deactivate"

train:
	$(PYTHON) slither_main.py --sessions 100 --load None --display on --explore yes --step off

evaluate:
	$(PYTHON) slither_main.py --sessions 10 --load models/q_table10000.pkl --display on --step off --explore no

stepit:
	$(PYTHON) slither_main.py --sessions 1 --load models/q_table10000.pkl --display on --step on --explore no

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: clean, activate, deactivate, setup, norm, stepit, evaluate, train, help

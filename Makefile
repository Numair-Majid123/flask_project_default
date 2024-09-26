.PHONY: setup run test clean

PYTHON := python3

VENV := venv
VENV_ACTIVATE := . $(VENV)/bin/activate

APP := app.py

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV_ACTIVATE) && pip install -r requirements.txt

run:
	$(VENV_ACTIVATE) && $(PYTHON) $(APP)

test:
	$(VENV_ACTIVATE) && pytest

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

db-init:
	$(VENV_ACTIVATE) && $(PYTHON) -c "from app import db; db.create_all()"

db-migrate:
	$(VENV_ACTIVATE) && flask db migrate

db-upgrade:
	$(VENV_ACTIVATE) && flask db upgrade

format:
	$(VENV_ACTIVATE) && black .

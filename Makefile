PYTHON := python3
VENV   := .venv
PIP    := $(VENV)/bin/python -m pip
FLASK  := $(VENV)/bin/flask

APP    := app.py
HOST   := 0.0.0.0
PORT   := 5000

.DEFAULT_GOAL := help

help:
	@echo "Commandes :"
	@echo "  make venv        -> crée le venv"
	@echo "  make install     -> installe les deps (Flask + requests) dans le venv"
	@echo "  make run         -> lance Flask (dev) sur $(HOST):$(PORT)"
	@echo "  make freeze      -> génère requirements.txt depuis le venv"
	@echo "  make clean       -> supprime le venv"
	@echo "  make deps-check  -> vérifie que Flask/requests sont bien dans le venv"

venv:
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@$(VENV)/bin/python -m ensurepip --upgrade >/dev/null 2>&1 || true
	@$(PIP) --version >/dev/null

install: venv
	@if [ -f requirements.txt ]; then \
		echo "Installation via requirements.txt"; \
		$(PIP) install -r requirements.txt; \
	else \
		echo "Pas de requirements.txt — installation minimale (flask + requests)"; \
		$(PIP) install flask requests; \
	fi

deps-check: venv
	@$(PYTHON) -c "import sys; print(sys.executable)"
	@$(VENV)/bin/python -c "import flask, requests; print('OK: flask', flask.__version__, '| requests', requests.__version__)"

run: install
	FLASK_APP=$(APP) FLASK_ENV=development $(FLASK) run --host=$(HOST) --port=$(PORT)

freeze: install
	$(PIP) freeze > requirements.txt
	@echo "requirements.txt mis à jour."

clean:
	rm -rf $(VENV)

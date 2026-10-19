PYTHON ?= python3
PORT ?= 8000
SCENARIO ?= supply-chain-siege

.DEFAULT_GOAL := help

.PHONY: help install install-dev run web doctor scenarios scenario-start scenario-verify test lint format-check build ci

help: ## Show the available development commands.
	@awk 'BEGIN {FS = ":.*## "; printf "GitQuest commands:\n\n"} /^[a-zA-Z_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install GitQuest into the active Python environment.
	$(PYTHON) -m pip install -e .

install-dev: ## Install GitQuest and its free development tools.
	$(PYTHON) -m pip install -e ".[dev]"

run: ## Start the terminal campaign.
	$(PYTHON) -m gitquest play

web: ## Start the local browser console (override with PORT=8765).
	$(PYTHON) -m gitquest web --port $(PORT)

doctor: ## Check which GitQuest runtime profiles are available.
	$(PYTHON) -m gitquest doctor

scenarios: ## List the installed incident scenarios.
	$(PYTHON) -m gitquest scenario list

scenario-start: ## Initialize SCENARIO in a fresh managed workspace.
	$(PYTHON) -m gitquest scenario start $(SCENARIO)

scenario-verify: ## Score the current SCENARIO remediation.
	$(PYTHON) -m gitquest scenario verify $(SCENARIO)

test: ## Run the dependency-free unit and integration test suite.
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

lint: ## Run Ruff's static checks (requires install-dev).
	$(PYTHON) -m ruff check src tests

format-check: ## Verify Ruff formatting without changing files.
	$(PYTHON) -m ruff format --check src tests

build: ## Build the wheel and source distribution (requires install-dev).
	$(PYTHON) -m build

ci: lint format-check test build ## Run the same quality gate used by GitHub Actions.

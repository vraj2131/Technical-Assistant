# =========================
# Knowledge Assistant Makefile
# =========================
# Usage:
#   make help            # list targets
#   make setup           # install deps
#   make qdrant-up       # start local Qdrant
#   make save-corpus     # (re)download docs (optional)
#   make index           # embed + upload vectors (to Qdrant)
#   make run             # launch Streamlit UI
#   make logs-app        # tail app logs
#   make test            # run tests
#   make clean-all       # clean caches, indexes, logs
#
# Pro tips:
# - Set PDF=1 to also render PDFs when saving corpus: `make save-corpus PDF=1`
# - Override PY if your interpreter is named differently: `make PY=python3 run`

SHELL := /bin/bash
.ONESHELL:

# --- Binaries (override if needed) ---
PY ?= python
PIP ?= pip
STREAMLIT ?= streamlit
DOCKER ?= docker

# --- Paths ---
APP := src/ui/app.py
ENV_FILE ?= .env

# --- Helper: export .env to subprocesses (bash-only) ---
define _load_env
	set -a; \
	if [ -f "$(ENV_FILE)" ]; then source "$(ENV_FILE)"; fi; \
	set +a;
endef

# --- Docker/Qdrant ---
QDRANT_CONTAINER ?= qdrant
QDRANT_IMAGE ?= qdrant/qdrant:latest
QDRANT_PORTS ?= -p 6333:6333 -p 6334:6334
QDRANT_VOLUME ?= -v "$(PWD)/qdrant_storage:/qdrant/storage"

# --- Flags ---
PDF ?= 0   # PDF=1 to enable --pdf on save_corpus

# Default target
.DEFAULT_GOAL := help

.PHONY: help
help: ## show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' Makefile | sed 's/:.*##/: /' | sort

# -------------------------
# Setup & housekeeping
# -------------------------
.PHONY: setup
setup: ## install python dependencies
	@$(call _load_env)
	$(PIP) install -U pip setuptools wheel
	@if [ -f requirements.txt ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		echo "requirements.txt not found; skipping."; \
	fi

.PHONY: dirs
dirs: ## create expected folders (logs, indexes)
	@mkdir -p logs/{app,ingestion,retrieval,rag,eval} indexes/faiss

.PHONY: format
format: ## format code (optional: needs black)
	@if command -v black >/dev/null 2>&1; then black src tests; else echo "black not installed"; fi

.PHONY: lint
lint: ## lint code (optional: needs ruff)
	@if command -v ruff >/dev/null 2>&1; then ruff check src tests; else echo "ruff not installed"; fi

# -------------------------
# Data ingestion
# -------------------------
.PHONY: save-corpus
save-corpus: ## download/update the 20 tech-doc URLs into data/ (HTML/MD and optional PDF)
	@$(call _load_env)
	@if [ "$(PDF)" = "1" ]; then \
		$(PY) src/ingestion/save_corpus.py --pdf; \
	else \
		$(PY) src/ingestion/save_corpus.py; \
	fi

# -------------------------
# Vector DB (Qdrant local)
# -------------------------
.PHONY: qdrant-up
qdrant-up: ## start local Qdrant (detached)
	@$(DOCKER) rm -f $(QDRANT_CONTAINER) >/dev/null 2>&1 || true
	$(DOCKER) run -d --name $(QDRANT_CONTAINER) $(QDRANT_PORTS) $(QDRANT_VOLUME) $(QDRANT_IMAGE)
	@echo "Qdrant started → http://localhost:6333"

.PHONY: qdrant-down
qdrant-down: ## stop & remove local Qdrant container
	@$(DOCKER) rm -f $(QDRANT_CONTAINER) || true
	@echo "Qdrant stopped."

.PHONY: qdrant-logs
qdrant-logs: ## tail Qdrant container logs
	@$(DOCKER) logs -f $(QDRANT_CONTAINER)

# -------------------------
# Indexing (embeddings + upload)
# -------------------------
.PHONY: index
index: dirs ## chunk + embed + upload vectors to Qdrant/FAISS per .env
	@$(call _load_env)
	$(PY) -m src.ingestion.build_index

# -------------------------
# App (Streamlit)
# -------------------------
.PHONY: run
run: ## launch Streamlit UI
	@$(call _load_env)
	$(STREAMLIT) run $(APP)

# -------------------------
# Logs
# -------------------------
.PHONY: logs-app logs-ingestion logs-retrieval logs-rag logs-eval
logs-app: ## tail app logs
	@tail -f logs/app/app.log
logs-ingestion: ## tail ingestion logs
	@tail -f logs/ingestion/ingestion.log
logs-retrieval: ## tail retrieval logs
	@tail -f logs/retrieval/retrieval.log
logs-rag: ## tail rag logs
	@tail -f logs/rag/rag.log
logs-eval: ## tail eval logs
	@tail -f logs/eval/eval.log

# -------------------------
# Tests & eval
# -------------------------
.PHONY: test
test: ## run pytest
	@if command -v pytest >/dev/null 2>&1; then pytest -q; else echo "pytest not installed"; fi

.PHONY: smoke
smoke: ## quick retrieval sanity checks (if implemented)
	@$(call _load_env)
	$(PY) -m src.eval.smoke_test

# -------------------------
# Clean
# -------------------------
.PHONY: clean-index clean-logs clean-all
clean-index: ## remove local indexes (FAISS) and cached artifacts
	@rm -rf indexes/faiss __pycache__ **/__pycache__ .pytest_cache .mypy_cache .pytype .pyre
clean-logs: ## remove logs
	@rm -rf logs && mkdir -p logs/{app,ingestion,retrieval,rag,eval}
clean-all: clean-index clean-logs ## nuke indexes and logs

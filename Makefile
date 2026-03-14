POETRY      = poetry
PY          = python3
MAIN        = main.py
OUTPUT_DIR  = data/output
LOCAL_HF_HOME = $(shell pwd)/.model_cache

MYPY_FLAGS  = --warn-return-any \
              --warn-unused-ignores \
              --ignore-missing-imports \
              --disallow-untyped-defs \
              --check-untyped-defs

.PHONY: install run clean dell lint

# Installation: Create a local venv
# Установка: создаем локальный venv
install:
	@echo "Installing dependencies..."
	$(PY) -m pip install poetry
	$(POETRY) config virtualenvs.in-project true
	$(POETRY) install
	@echo "Installation complete."

# Launch: Passing an environment variable directly to the process
# Запуск: прокидываем переменную окружения прямо в процесс
run:
	@echo "Starting with HF_HOME=$(LOCAL_HF_HOME)"
	HF_HOME=$$(pwd)/.model_cache $(POETRY) run $(PY) main.py

# Lint check
# Линт проверка
lint:
	@echo "Running flake8 (syntax & logic)..."
	$(POETRY) run flake8 . --exclude .venv,llm_sdk --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "Running mypy (type annotations)..."
	$(POETRY) run mypy . $(MYPY_FLAGS) --exclude ".venv|llm_sdk"

# Cleaning temporary files
# Очистка временных файлов
clean:
	@echo "Cleaning outputs..."
	rm -rf $(OUTPUT_DIR)/*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

# Completely remove .venv and model weight
# Полное удаление .venv и веса модели
dell: clean
	@echo "Deleting virtual environment and models..."
	rm -rf .venv
	rm -rf $(LOCAL_HF_HOME)
	@echo "Project directory is clean and light."
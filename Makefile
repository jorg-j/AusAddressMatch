#.ONESHELL:

#.PHONY: install

PYTHON = python3
POETRY = poetry
DIR = aussieaddress


.PHONY: poetryinstall
poetryinstall: poetry.lock

# Check if poetry.lock is modified
poetry.lock: pyproject.toml
	@echo "Checking for changes in dependencies..."
	@if [ -e $@ ] && ! cmp -s $@ <(poetry lock); then \
		echo "Dependencies have changed. Running 'poetry install' to update."; \
		$(POETRY) install; \
	else \
		echo "No changes in dependencies. Skipping installation."; \
	fi

doctests: poetryinstall
	poetry run python3 -m doctest $(DIR)/compare.py



.PHONY: update
update:
	$(POETRY) update

.PHONY: add
add:
	$(POETRY) add

.PHONY: remove
remove:
	$(POETRY) remove

.PHONY: lock
lock:
	$(POETRY) lock

.PHONY: test
test:
	$(POETRY) run pytest

.PHONY: lint
lint:
	$(POETRY) run flake8

.PHONY: format
format:
	$(POETRY) run black .

.PHONY: clean
clean:
	$(POETRY) run rm -rf dist build

.PHONY: build
build: clean
	$(POETRY) build

.PHONY: publish
publish: build
	$(POETRY) publish


.PHONY: env
env:
	python3 -m venv env
	source env/bin/activate
	pip install -r requirements.txt

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install	- Install project dependencies"
	@echo "  update	 - Update project dependencies"
	@echo "  add		- Add a new dependency"
	@echo "  remove	 - Remove a dependency"
	@echo "  lock	   - Update and lock the dependencies"
	@echo "  test	   - Run tests"
	@echo "  lint	   - Lint code"
	@echo "  format	 - Format code"
	@echo "  clean	  - Clean up build artifacts"
	@echo "  build	  - Build the project"
	@echo "  publish	- Publish the project to PyPI"
	@echo "  help	   - Show this help message"

# Default target
.DEFAULT_GOAL := help
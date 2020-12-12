PYTHON     = python3.8 -m pipenv run
SRC_FILES := $(shell find . -name "*.py")
LOCK       = Pipfile.lock

.PHONY: help
help:
	@echo "Usage:"
	@echo "    help:         Prints this screen"
	@echo "    install-deps: Installs dependencies in the internal venv"
	@echo "    check-fmt:    Checks the code for style issues"
	@echo "    fmt:          Make the formatting changes directly to the project"
	@echo "    lint:         Lints the code"
	@echo "    test:         Tests the code"
	@echo "    run:          Run the development version of the app"
	@echo "    prod-build:   Build the production version of the app"
	@echo "    prod-run:     Run the production version of the app"
	@echo "    clean:        Clean out temporaries"
	@echo "    clean-full:   Clean out temporaries and the internal venv"
	@echo ""

.PHONY: install-deps
install-deps:
	$(PYTHON) pipenv install --dev

$(LOCK):
	$(PYTHON) pipenv lock --pre --clear
	make install-deps

.PHONY: update-deps
update-deps:
	rm $(LOCK)
	make $(LOCK)

.PHONY: check-fmt
check-fmt:
	@echo "Format Checking"
	$(PYTHON) black --check .

.PHONY: fmt
fmt:
	@echo "Auto Formatting"
	$(PYTHON) black .

.PHONY: lint
lint:
	@echo "Type Checking"
	@$(PYTHON) mypy --ignore-missing-imports $(SRC_FILES)
	@echo "Linting"
	@$(PYTHON) pylint $(SRC_FILES)

.PHONY: test
test:
	 $(PYTHON) pytest tests

.PHONY: run
run:
	FLASK_APP=coa_flask_app FLASK_ENV=development $(PYTHON) flask run

.PHONY: prod-build
prod-build:
	docker build . -t coa-back-end

.PHONY: prod-run
prod-run: prod-build
	docker run -p 5000:80 -e DB_USERNAME -e DB_PASSWORD -e DB_SERVER -e DB_DATABASE -e DB_PORT coa-back-end

.PHONY:
clean:
	@echo "Removing temporary files"
	@rm -rf "*.pyc" "__pycache__" ".mypy_cache" ".pytest_cache"

.PHONY: clean-full
clean-full: clean
	@echo "Removing virtual environment"
	@pipenv --rm clean

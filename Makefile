SHELL=/bin/bash

.PHONY: multitimer
multitimer:
	python3 ./multitimer.py

.PHONY: multistopwatch
multistopwatch:
	python3 ./multistopwatch.py

.PHONY: pipinstall
pipinstall:
	pip install --upgrade pip
	pip install -r requirements.txt 

.PHONY: docker-build
docker-build:
	docker build -t multistopwatch .

.PHONY: docker-run
docker-run:
	docker run -it -p 8080:8080 multistopwatch

.PHONY: docker-build-and-run
docker-build-and-run:
	docker build -t multistopwatch . && docker run -it -p 8080:8080 multistopwatch

.PHONY: createvenv
createvenv:
	python3 -m venv .venv
	@echo "Please run << source .venv/bin/activate >> in your terminal"

.PHONY: pylint
pylint:
	pylint *.py

.PHONY: flake8
flake8:
	flake8 *.py

.PHONY pydocstyle:
pydocstyle:
	pydocstyle *.py

.PHONY: linters
linters: flake8 pylint pydocstyle

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

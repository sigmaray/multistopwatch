.PHONY: pylint
pylint:
	pylint *.py --max-line-length=120 --disable=invalid-name,duplicate-code,no-name-in-module,too-many-arguments,c-extension-no-member

.PHONY: flake8
flake8:
	flake8 *.py

.PHONY pydocstyle:
pydocstyle:
	pydocstyle *.py

.PHONY: linters
linters: flake8 pylint pydocstyle

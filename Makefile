# test

coverage-html:
	coverage html --fail-under 100

coverage-report:
	coverage report -m

test:
	flake8 orders
	coverage run -m pytest */test $(ARGS)

coverage: test coverage-report coverage-html

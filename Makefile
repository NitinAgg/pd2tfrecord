lint:
	pipenv run isort
	pipenv run black .
	pipenv run flake8
	pipenv run mypy .

lint-test:
	pipenv run isort --check-only
	pipenv run flake8
	pipenv run mypy .

test: lint-test
	coverage run
	coverage report

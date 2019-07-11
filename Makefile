help:
	@echo "Usage:"
	@echo "    make help        show this message"
	@echo "    make init        create virtual environment and install dependencies"
	@echo "    make setup       do migrations and collect static files"
	@echo "    make activate    enter virtual environment"
	@echo "    make test        run the test suite"
	@echo "    exit             leave virtual environment"

init:
	pip3 install pipenv --user
	pipenv install --dev --three

setup:
	cp laumproject/settings.py.sample laumproject/settings.py
	pipenv run python ./manage.py migrate
	pipenv run python ./manage.py collectstatic
	pipenv run python ./manage.py compilemessages

activate:
	pipenv shell

test:
	pipenv run coverage erase
	pipenv run ./manage.py test
	pipenv run coverage run ./manage.py test
	pipenv run coverage report

.PHONY: help activate test

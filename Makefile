help:  - make activate
	@echo "Usage:"
	@echo "    make help        show this message"
	@echo "    make init        create virtual environment and install dependencies"
	@echo "    make setup       do migrations and collect static files"
	@echo "    make activate    enter virtual environment"
	@echo "    make test        run the test suite"
	@echo "    exit             leave virtual environment"

init:
	pip install pipenv
	pipenv install --dev --three

setup:
	cp laum/settings.py.sample laum/settings.py
	./manage.py migrate
	./manage.py collectstatic

activate:
	pipenv shell

test:
	coverage erase
	./manage.py test
	coverage run ./manage.py test
	coverage report

.PHONY: help activate test

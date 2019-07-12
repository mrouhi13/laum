help:
	@echo "Usage:"
	@echo "    make help        show this message"
	@echo "    make init        create virtual environment and install dependencies"
	@echo "    make setup       do migrations and collect static files"
	@echo "    make activate    enter virtual environment"
	@echo "    make test        run the test suite"
	@echo "    exit             leave virtual environment"

init:
	pip3 install pipenv
	pipenv install --dev --three

setup:
    mkdir log
    cp laumproject/settings.py.sample laumproject/settings.py
    psql -c "CREATE DATABASE $DATABASE_NAME;" -U $DATABASE_USER
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

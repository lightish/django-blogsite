# change that var if your virtual env dir is not named venv in the project root
VIRTUAL_ENV_PATH := ./venv


run:
	python manage.py runserver


# MAKE SURE VIRTUAL_ENV_PATH is set up correctly
# make sure you run it inside your virtual environment
resetm: purge-migrations clear-media migrate


purge-migrations:
	@echo 'Cleaning up...'
	find . -path ./venv -prune -o -wholename '*/migrations/*' -not -wholename '*/migrations/__init__.py' -exec rm -f {} \;
	rm -f db.sqlite3


clear-media:
	rm -rf media/*


migrate:
	@echo 'Making new migrations...'
	python manage.py makemigrations
	python manage.py migrate


unsec-admin:
	python manage.py createsuperuser --username 'admin' --email 'admin@mail.com'

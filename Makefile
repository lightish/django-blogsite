run:
	python backend/manage.py runserver


resetm: purge-migrations clear-media migrate


purge-migrations:
	@echo 'Cleaning up...'
	-find backend/ -wholename '*/migrations/*' -not -wholename '*/migrations/__init__.py' -exec rm -rf {} \;
	rm -f backend/db.sqlite3


clear-media:
	rm -rf backend/media/*


migrate:
	@echo 'Making new migrations...'
	python backend/manage.py makemigrations
	python backend/manage.py migrate


unsec-admin:
	python backend/manage.py createsuperuser --username 'admin' --email 'admin@mail.com'

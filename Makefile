
install:
	@pip install -r requirements.txt

freeze:
	@pip freeze > requirements.txt

shell:
	@python manage.py shell

dbshell:
	@python manage.py dbshell

dev:
	@python manage.py runserver

assets:
	@python manage.py collectstatic
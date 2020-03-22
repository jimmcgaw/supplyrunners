
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

ssl:
	@python manage.py runsslserver

sslcert:
	@python manage.py runsslserver --certificate cert/supplyrunners.dev.crt --key cert/supplyrunners.dev.key

assets:
	@python manage.py collectstatic
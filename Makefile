ruff:
	ruff format && ruff check . --fix

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver localhost:8000

test:
	pytest --cache-clear

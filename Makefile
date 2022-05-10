build:
	docker-compose build

down:
	docker-compose down

up: build migrate
	docker-compose up -d

migrate:
	docker-compose run api python manage.py migrate

mami:
	docker-compose run api python manage.py makemigrations

deps:
	docker-compose run api poetry install

bash:
	docker-compose run api /bin/sh

test: build migrate
	docker-compose run api python manage.py test

coverage: build migrate
	docker-compose run api coverage run --source='api' --omit='api/tests/*' manage.py test
	docker-compose run api coverage report
	docker-compose run api coverage xml

ifneq (,w$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env
endif

build:
	docker-compose up --build -d --remove-orphans

p-build:
	docker-compose  -f docker-compose.prod.yml up --build -d --remove-orphans

p-up:
	docker-compose  -f docker-compose.prod.yml up -d --remove-orphans

p-down:
	docker-compose  -f docker-compose.prod.yml down

up:
	docker-compose up -d

stop:
	docker-compose stop

down:
	docker-compose down

logs:
	docker-compose logs

down-volumes:
	docker-compose down -v

shell:
	docker-compose exec web /opt/venv/bin/python manage.py shell

check-services:
	docker ps -a

migrate:
	docker-compose exec web /opt/venv/bin/python manage.py migrate

install-all:
	docker-compose exec web /opt/venv/bin/pip install -r requirements.txt

rebuild-index:
	docker-compose exec web /opt/venv/bin/python manage.py rebuild_index --noinput

update-index:
	docker-compose exec web /opt/venv/bin/python manage.py update_index
p-install-all:
	docker-compose -f docker-compose.prod.yml exec web /opt/venv/bin/pip install -r requirements.txt

p-migrate:
	docker-compose -f docker-compose.prod.yml exec web /opt/venv/bin/python manage.py migrate

p-makemigrations:
	docker-compose -f docker-compose.prod.yml exec web /opt/venv/bin/python manage.py makemigrations

p-static:
	docker-compose -f docker-compose.prod.yml exec web /opt/venv/bin/python manage.py collectstatic

static:
	docker-compose exec web /opt/venv/bin/python manage.py collectstatic

runlocal:
	docker-compose exec web /opt/venv/bin/python manage.py runserver 8000

makemigrations:
	docker-compose exec web /opt/venv/bin/python manage.py makemigrations

p-superuser:
	docker-compose -f docker-compose.prod.yml exec web /opt/venv/bin/python manage.py createsuperuser

init-admin:
	docker-compose -f docker-compose.prod.yml exec web /opt/venv/bin/python manage.py initadmin

superuser:
	docker-compose exec web /opt/venv/bin/python manage.py createsuperuser

# e.g make startapp ARGS="appointments"
startapp:
	docker-compose exec web /opt/venv/bin/python manage.py startapp $(ARGS)

coverage-test:
	docker-compose exec web /opt/venv/bin/coverage run manage.py test

pytest:
	docker-compose exec web /opt/venv/bin/coverage run -m pytest

coverage-html:
	docker-compose exec web /opt/venv/bin/coverage html

coverage-badge:
	docker-compose exec web /opt/venv/bin/coverage-badge -o docs/coverage.svg -f

celery-worker:
	docker-compose exec web /opt/venv/bin/python -m celery -A core worker -l info

#docker-compose exec web /opt/venv/bin/python -m celery -A core worker --loglevel=info -P eventlet
#celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
DOCKER-COMPOSE = docker-compose -f infrastructure/docker-compose.yml --project-directory .

install:
	pip install pipenv
	pipenv install --dev

start: install
	pipenv run gunicorn -c infrastructure/gunicorn.conf.py -b :80 pepy.infrastructure.web.__init__:app

start-containers:
	$(DOCKER-COMPOSE) up -d
	until curl --silent -XGET --fail http://localhost:5200/health-check; do printf '.'; sleep 1; done

stop-containers:
	$(DOCKER-COMPOSE) stop

remove-containers:
	$(DOCKER-COMPOSE) down

unit-tests:
	$(DOCKER-COMPOSE) exec pepy pipenv run pytest tests/unit

integration-tests:
	$(DOCKER-COMPOSE) exec pepy pipenv run pytest tests/integration

acceptance-tests:
	$(DOCKER-COMPOSE) exec pepy pipenv run behave tests/acceptance

tests: unit-tests  acceptance-tests

format-code:
	$(DOCKER-COMPOSE) exec pepy pipenv run black -l 120 --exclude=".*\/node_modules" pepy/ tests/


DOCKER_TAG?=latest
DOCKER-COMPOSE = PEPY_VERSION=$(DOCKER_TAG) docker-compose -f infrastructure/docker-compose.yml --project-directory .
params?=

start-containers:
	$(DOCKER-COMPOSE) up -d
	until curl --silent -XGET --fail http://localhost:5200/health-check; do sleep 1; done

stop-containers:
	$(DOCKER-COMPOSE) stop

remove-containers:
	$(DOCKER-COMPOSE) down

unit-tests:
	$(DOCKER-COMPOSE) exec $(params) pepy-test pytest tests/unit

integration-tests:
	$(DOCKER-COMPOSE) exec $(params) pepy-test pytest -v tests/integration

acceptance-tests:
	$(DOCKER-COMPOSE) exec $(params) pepy-test behave tests/acceptance

tests: unit-tests integration-tests acceptance-tests

format-code:
	pipenv run black -l 120 --exclude=".*\/node_modules" pepy/ tests/


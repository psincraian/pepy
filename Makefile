install:
	pip install -r requirements.txt

start: install
	gunicorn -c infrastructure/gunicorn.conf.py -b :80 pepy.infrastructure.web.__init__:app

start-containers:
	docker-compose -f infrastructure/docker-compose.yml --project-directory . up -d

stop-containers:
	docker-compose -f infrastructure/docker-compose.yml --project-directory . stop

remove-containers:
	docker-compose -f infrastructure/docker-compose.yml --project-directory . down

migrations:
	docker-compose -f infrastructure/docker-compose.yml --project-directory . exec pepy yoyo apply --database "postgresql://pepy:pepy@pgsql/pepy" infrastructure/migrations/ --no-config-file --batch
	docker-compose -f infrastructure/docker-compose.yml --project-directory . exec pepy yoyo apply --database "postgresql://pepy:pepy@pgsql/pepy_test" infrastructure/migrations/ --no-config-file --batch

unit-tests:
	docker-compose -f infrastructure/docker-compose.yml --project-directory . exec pepy pytest tests/unit

integration-tests:
	docker-compose -f infrastructure/docker-compose.yml --project-directory . exec pepy pytest tests/integration

acceptance-tests:
	docker-compose -f infrastructure/docker-compose.yml --project-directory . exec pepy behave tests/acceptance

tests: unit-tests integration-tests acceptance-tests


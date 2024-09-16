app_port = 8080

run:
	docker run -p ${app_port}:${app_port} --env-file ./.env 'tender_app'

build: env_file
	docker build --tag 'tender_app' .

env_file:
ifeq (,$(wildcard .env))
	@echo "Creating .env file from .env-example..."
	cp .env-example .env
endif

clean:
	docker stop $(shell docker ps -q --filter ancestor=tender_app ) 2>/dev/null || true
	docker rm $(shell docker ps -a -q --filter "ancestor=tender_app") 2>/dev/null || true

rebuild: clean build

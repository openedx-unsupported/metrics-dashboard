.DEFAULT_GOAL := help

.PHONY: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo ""
	@echo "These should be run from outside the container:"
	@echo ""
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*? # .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.* # "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'
	@echo ""

# -----------------------------------------------------------------------------
# local devstack

requirements:
	# python3.9 venv
	pip install -r requirements.txt

dev.up: .setup .up  # Start containers

dev.down: .down  # Stop containers

dev.clean: .down .clean  # Stop containers and remove all persistent data

# -----------------------------------------------------------------------------
# sir mordred

mordred.logs: CONTAINER_ID='experimental_mordred_1'
mordred.logs: .logs  # Tail mordred logs

mordred.shell: CONTAINER_ID='experimental_mordred_1'
mordred.shell: .shell  # Open shell on the mordred container

mordred.restart: CONTAINER_ID='experimental_mordred_1'
mordred.restart: .restart  # Restart the mordred container

mordred.destroy: CONTAINER_ID='experimental_mordred_1'
mordred.destroy: .destroy  # Destroy the mordred container

# -----------------------------------------------------------------------------
# hatstall

hatstall.logs: CONTAINER_ID='experimental_hatstall_1'
hatstall.logs: .logs  # Tail hatstall logs

hatstall.shell: CONTAINER_ID='experimental_hatstall_1'
hatstall.shell: .shell  # Open shell on the hatstall container

hatstall.restart: CONTAINER_ID='experimental_hatstall_1'
hatstall.restart: .restart  # Restart the hatstall container

hatstall.destroy: CONTAINER_ID='experimental_hatstall_1'
hatstall.destroy: .destroy  # Destroy the hatstall container

# -----------------------------------------------------------------------------
# kibiter

kibiter.logs: CONTAINER_ID='experimental_kibiter_1'
kibiter.logs: .logs  # Tail kibiter logs

kibiter.shell: CONTAINER_ID='experimental_kibiter_1'
kibiter.shell: .shell  # Open shell on the kibiter container

kibiter.restart: CONTAINER_ID='experimental_kibiter_1'
kibiter.restart: .restart  # Restart the kibiter container

kibiter.destroy: CONTAINER_ID='experimental_kibiter_1'
kibiter.destroy: .destroy  # Destroy the kibiter container

# -----------------------------------------------------------------------------
# elasticsearch

elasticsearch.logs: CONTAINER_ID='experimental_elasticsearch_1'
elasticsearch.logs: .logs  # Tail elasticsearch logs

elasticsearch.shell: CONTAINER_ID='experimental_elasticsearch_1'
elasticsearch.shell: .shell  # Open shell on the elasticsearch container

elasticsearch.restart: CONTAINER_ID='experimental_elasticsearch_1'
elasticsearch.restart: .restart  # Restart the elasticsearch container

elasticsearch.destroy: CONTAINER_ID='experimental_elasticsearch_1'
elasticsearch.destroy: .destroy  # Destroy the elasticsearch container

# -----------------------------------------------------------------------------
# mariadb

mariadb.logs: CONTAINER_ID='experimental_mariadb_1'
mariadb.logs: .logs  # Tail mariadb logs

mariadb.shell: CONTAINER_ID='experimental_mariadb_1'
mariadb.shell: .shell  # Open shell on the mariadb container

mariadb.restart: CONTAINER_ID='experimental_mariadb_1'
mariadb.restart: .restart  # Restart the mariadb container

mariadb.destroy: CONTAINER_ID='experimental_mariadb_1'
mariadb.destroy: .destroy  # Destroy the mariadb container

# -----------------------------------------------------------------------------
# utilities

.up:
	docker-compose up -d

.down:
	docker-compose down

.logs:
	docker logs -f $(CONTAINER_ID)

.shell:
	docker exec -it $(CONTAINER_ID) env TERM=xterm /bin/bash

.restart:
	docker restart $(CONTAINER_ID)

.stop:
	docker stop $(CONTAINER_ID)

.destroy: .stop
	docker rm $(CONTAINER_ID)

.clean:
	rm -rf $(shell pwd)/es-data/nodes

.fix-permissions:
	# Fix permissions on log dir so mordred can write to it
	chmod 777 $(shell pwd)/logs

.setup: .fix-permissions

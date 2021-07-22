.DEFAULT_GOAL := help

.PHONY: clean help requirements

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo ""
	@echo "These should be run from outside the container:"
	@echo ""
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*? # .*$$)' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.* # "); {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2)'
	@echo ""

# grimoirelab Docker configuration
GRIMOIRE_DOCKER_IMAGE_LOCAL?=grimoirelab/full
GRIMOIRE_DOCKER_IMAGE_REMOTE?=grimoirelab/installed
GRIMOIRE_HOST?=0.0.0.0
GRIMOIRE_PORT?=5601
GRIMOIRE_DOCKER_ARGS?=--tty --detach

GRIMOIRE_CONTAINER_ID_LOCAL:=$(shell docker ps -a -q --filter ancestor=$(GRIMOIRE_DOCKER_IMAGE_LOCAL))
GRIMOIRE_CONTAINER_ID_REMOTE:=$(shell docker ps -a -q --filter ancestor=$(GRIMOIRE_DOCKER_IMAGE_REMOTE))

# Run full grimoirelab container, with all services running locally

start: .setup  # Start grimoirelab/full container
	docker run \
		--publish $(GRIMOIRE_HOST):$(GRIMOIRE_PORT):$(GRIMOIRE_PORT) \
		--volume $(shell pwd)/dashboard.cfg:/dashboard.cfg \
		--volume $(shell pwd)/project.cfg:/project.cfg \
		--volume $(shell pwd)/aliases.json:/aliases.json \
		--volume $(shell pwd)/credentials.cfg:/override.cfg \
		--volume $(shell pwd)/projects-devstack.json:/projects.json \
		--volume $(shell pwd)/logs:/logs \
		--volume $(shell pwd)/es-data:/var/lib/elasticsearch \
		$(GRIMOIRE_DOCKER_ARGS) \
		$(GRIMOIRE_DOCKER_IMAGE_LOCAL)

shell: GRIMOIRE_CONTAINER_ID=$(GRIMOIRE_CONTAINER_ID_LOCAL)
shell: .shell  # Open shell on the grimoirelab/full container

pull: GRIMOIRE_DOCKER_IMAGE=$(GRIMOIRE_DOCKER_IMAGE_LOCAL)
pull: .pull  # Update grimoirelab/full docker image

restart: GRIMOIRE_CONTAINER_ID=$(GRIMOIRE_CONTAINER_ID_LOCAL)
restart: .restart # Restart grimoirelab/full container

stop: GRIMOIRE_CONTAINER_ID=$(GRIMOIRE_CONTAINER_ID_LOCAL)
stop: .stop  # Stop grimoirelab/full container

destroy: GRIMOIRE_CONTAINER_ID=$(GRIMOIRE_CONTAINER_ID_LOCAL)
destroy: .destroy  # Delete grimoirelab/full container

clean: destroy  # Delete grimoirelab/full container and remove all persistent elasticsearch data

# -----------------------------------------------------------------------
# Remote: Connect to remote databases

start.remote: .setup  # Start grimoirelab container, connected to remote production databases.
	docker run \
		--publish $(GRIMOIRE_HOST):$(GRIMOIRE_PORT):$(GRIMOIRE_PORT) \
		--volume $(shell pwd)/dashboard.cfg:/dashboard.cfg \
		--volume $(shell pwd)/infra.cfg:/infra.cfg \
		--volume $(shell pwd)/project.cfg:/project.cfg \
		--volume $(shell pwd)/credentials.cfg:/override.cfg \
		--volume $(shell pwd)/aliases.json:/aliases.json \
		--volume $(shell pwd)/identities.json:/identities.json \
		--volume $(shell pwd)/projects.json:/projects.json \
		--volume $(shell pwd)/logs:/logs \
		$(GRIMOIRE_DOCKER_ARGS) \
		$(GRIMOIRE_DOCKER_IMAGE_REMOTE)

shell.remote: GRIMOIRE_CONTAINER_ID=$(GRIMOIRE_CONTAINER_ID_REMOTE)
shell: .shell  # Open shell on the grimoirelab/installed container

pull.remote: GRIMOIRE_DOCKER_IMAGE=$(GRIMOIRE_DOCKER_IMAGE_REMOTE)
pull: .pull  # Update grimoirelab/installed docker image

restart.remote: GRIMOIRE_CONTAINER_ID=$(GRIMOIRE_CONTAINER_ID_REMOTE)
restart: .restart # Restart grimoirelab/installed container

stop.remote: GRIMOIRE_CONTAINER_ID=$(GRIMOIRE_CONTAINER_ID_REMOTE)
stop: .stop  # Stop grimoirelab/installed container

destroy.remote: GRIMOIRE_CONTAINER_ID=$(GRIMOIRE_CONTAINER_ID_REMOTE)
destroy: .destroy  # Delete grimoirelab/installed container

# ----------------------------------------------------------------
# utilities

.shell:
	docker exec -it $(GRIMOIRE_CONTAINER_ID) env TERM=xterm /bin/bash

.pull:
	docker pull $(GRIMOIRE_DOCKER_IMAGE)

.restart:
	docker restart $(GRIMOIRE_CONTAINER_ID)

.stop:
	docker stop $(GRIMOIRE_CONTAINER_ID)

.destroy: stop
	docker rm $(GRIMOIRE_CONTAINER_ID)

.clean:
	rm -rf $(shell pwd)/es-data/nodes

.fix-permissions:
	# Fix permissions on log dirs so grimoire can write to it
	chmod 777 $(shell pwd)/logs

.setup: .fix-permissions

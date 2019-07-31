FROM grimoirelab/installed

USER root

RUN apt-get update

RUN pip3 install slackclient
RUN pip3 install github3.py

# clone git repo
RUN git clone https://github.com/openedx/metrics-dashboard.git ../../metrics-dashboard

# remove grimoirelabs files that are unnecessary
RUN rm ../../infra.cfg && \
	rm ../../dashboard.cfg && \
	rm ../../aliases.json
#	rm ../../identities.yaml && \

# copy our files to correct location
RUN cp /metrics-dashboard/set_config.py ../.. && \
	cp /metrics-dashboard/entrypoint.sh ../.. && \
	cp /metrics-dashboard/get_projects.py ../.. && \
	cp /metrics-dashboard/create_identities.py ../.. && \
	cp /metrics-dashboard/infra.cfg ../.. && \
	cp /metrics-dashboard/aliases.json ../.. && \
	cp /metrics-dashboard/dashboard.cfg ../.. && \
	cp /metrics-dashboard/og_projects.json ../.. && \
	cp /metrics-dashboard/create_dashboard.py ../..



RUN chmod 755 ../../entrypoint.sh

USER ${DEPLOY_USER}

# Entrypoint (mordred)
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "-c", "/infra.cfg", "/dashboard.cfg", "/project.cfg", "/override.cfg"]
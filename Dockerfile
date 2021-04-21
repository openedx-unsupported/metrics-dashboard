FROM grimoirelab/installed

USER root

RUN apt-get update
RUN apt-get -y install build-essential libffi-dev libssl-dev zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev

# Need a newer version of Python what ship in the base container.
# github3 uses "f" strings for one.
RUN curl -O https://www.python.org/ftp/python/3.9.4/Python-3.9.4.tgz
RUN tar -xf Python-3.9.4.tgz
RUN cd Python-3.9.4 && \
    ./configure --enable-optimizations && \
    make -j 4 && \
    make install

RUN pip3.9 install slackclient github3.py pyyaml

# clone git repo
# why do this, explains why my local updates made no difference...
RUN git clone https://github.com/openedx/metrics-dashboard.git ../../metrics-dashboard

RUN pwd

# remove grimoirelabs files that are unnecessary
RUN rm ../../infra.cfg && \
	rm ../../dashboard.cfg && \
	rm ../../aliases.json && \
	rm ../../identities.yaml

# copy our files to correct location

RUN cp /metrics-dashboard/set_config.py ../.. && \
	cp /metrics-dashboard/entrypoint.sh ../.. && \
	cp /metrics-dashboard/get_projects.py ../.. && \
	cp /metrics-dashboard/create_identities.py ../.. && \
	cp /metrics-dashboard/infra.cfg ../.. && \
	cp /metrics-dashboard/aliases.json ../.. && \
	cp /metrics-dashboard/dashboard.cfg ../.. && \
	cp /metrics-dashboard/og_projects.json ../.. && \
	cp /metrics-dashboard/create_dashboard.py ../.. && \
	cp -a /metrics-dashboard/dashboards ../..


RUN chmod 755 ../../entrypoint.sh

USER ${DEPLOY_USER}

# Entrypoint (mordred)
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "-c", "/infra.cfg", "/dashboard.cfg", "/project.cfg", "/override.cfg"]
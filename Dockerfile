FROM grimoirelab/installed

USER root

RUN pip3 install slackclient
RUN pip3 install PyGithub

# clone git repo
RUN git clone https://github.com/openedx/metrics-dashboard.git ../../metrics-dashboard

# remove grimoirelabs files that are unnecessary

#RUN rm ../../identities.yaml
RUN rm ../../infra.cfg
RUN rm ../../dashboard.cfg

# copy our files to correct location

RUN cp /metrics-dashboard/infra.cfg ../..
RUN cp /metrics-dashboard/dashboard.cfg ../..
#RUN cp /metrics-dashboard/identities.yaml ../..
RUN cp /metrics-dashboard/og_projects.json ../..
RUN cp /metrics-dashboard/create_dashboard.py ../..
RUN cp /metrics-dashboard/set_config.py ../..
RUN cp /metrics-dashboard/entrypoint.sh ../..
RUN cp /metrics-dashboard/get_projects.py ../..

RUN sudo chmod 755 ../../entrypoint.sh

USER ${DEPLOY_USER}

# Entrypoint (mordred)
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "-c", "/infra.cfg", "/dashboard.cfg", "/project.cfg", "/override.cfg"]
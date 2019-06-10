# metrics-dashboard
Dashboard for Open edX intended to run in a docker container by Grimoirelabs.

##How to Use
In order to run, use this command:

```
docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:5601:5601 \
    -v $(pwd)/logs:/logs \
    -v $(pwd)/credentials.cfg:/override.cfg \
    -v $(pwd)/projects.json:/projects.json \
    -v $(pwd)/dashboard.cfg:/dashboard.cfg \
    -v $(pwd)/orgs.json:/orgs.json \
    -v $(pwd)/infra.cfg:/infra.cfg \
    -t grimoirelab/full
```
[GrimoireLab Documentation] (https://github.com/chaoss/grimoirelab/tree/master/docker)

##File Notes
Notes on volumes

###logs/
In order to see the logs from all programs running in the container (i.e. Perceval, Sortinghat, SirMordred), you must have a local directory named logs. 

###credentials.cfg
The file credentials.cfg must contain a Github api token and a slack legacy api token. It should look like the following:

```
[github]
api-token = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

[slack]
api-token = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
###dashboard.cfg
Contains information regarding dashboard structure

###projects.json
Contains information (urls, id's) about information being gathered from named sources

###infra.cfg
Contains information regarding data collection

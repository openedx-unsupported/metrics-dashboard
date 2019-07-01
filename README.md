# metrics-dashboard
Dashboard for Open edX intended to run in a docker container by Grimoirelabs.

## How to Use
In order to run locally, use this command:

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
[GrimoireLab Documentation](https://github.com/chaoss/grimoirelab/tree/master/docker)

## File Notes
Notes on volumes

### logs/
In order to see the logs from all programs running in the container (i.e. Perceval, Sortinghat, SirMordred), you must have a local directory named logs. 

### credentials.cfg
The file credentials.cfg must contain a Github api token and a slack legacy api token. It should look like the following:

```
[github]
api-token = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

[slack]
api-token = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
### dashboard.cfg
Contains information regarding dashboard structure

### projects.json
Contains information (urls, id's) about information being gathered from named sources

### infra.cfg
Contains information regarding data collection

## Notes on scripts

### Saving changes to dashboards locally
If you would like to save changes to dashboards locally, or import local dashboards to kibana, use manage_dashboards.py.
If you run the program from the terminal, it expects to have 1 argument, either "import" or "export" to specify what action it should take. It will look for a folder called "dashboards" located in the same directory.

### Getting all repos from an organization, or all channels from a Slack workspace
You may find it easier to specify one organization for a grimoirelabs project, rather than specifying each individual repo. If this is the case create_dashboard.py will make that process easier. This script will look for a file called og_projects.json, and use the information in that file to overwrite projects.json. 

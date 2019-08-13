# metrics-dashboard #
Dashboard for Open edX intended to run in a docker container. 

Link for admin access (must enter username and password):https://66f663f015aecb785655faf0aae52d04.us-east-1.aws.found.io:9243

Link for read only access (anonymous access): https://openedx-metrics.herokuapp.com

# Components #
## GrimoireLab ##
Created by [Bitergia](https://bitergia.com/about/), GrimoireLab is open source software that can be used for data analytics. The specific software used in the metrics dashboard project is comprised of several parts, which are outlined in the [GrimoireLab tutorial](https://chaoss.github.io/grimoirelab-tutorial/README.html).

This project relies most directly on SirMordred, a piece of GrimoireLab's software that orchestrates the gathering and enriching of data from Git, Github, Slack, etc. and also produces the dashboards for Kibana.

### Configuration Files for GrimoireLab ###

* dashboard.cfg
	* Contains information relevant to data sources in Elasticsearch (i.e. index names), general information about data collection
* infra.cfg
	* Contains sensitive information about Elasticsearch, Kibana, and MariaDB
* override.cfg or credentials.cfg
	* Contains Github and Slack API keys. The Slack key must be a legacy token. 
* projects.json
	* Outlines which data sources to pull from
* identities.yaml
	* Maps individual people to usernames, emails, and organizations

## Docker ##

In addition to providing the software for GrimoireLab, Bitergia also maintains several dockerfiles for running the software. The metrics dashboard dockerfile uses the [grimoirelab/installed](https://hub.docker.com/r/grimoirelab/installed) dockerfile as its base image and other files and configurations are added or removed on top of the base. The metrics dashboard dockerfile itself should rarely need to be modified, although the sources it pulls from can be modified more often for any project configuration changes.

### Building Dockerfile ###

Should changes be made to the Dockerfile itself or to files in the GitHub repository, the Dockerfile will need to be rebuilt and pushed to Heroku. 

**Please note: if the changes you are making include adding a new section to Kibana, please go to Adding a New Section to Kibana before rebuilding the image.**

To rebuild the Dockerfile, use the command in the project directory:

```
docker build --tag=test_dockerfile --no-cache .
```

The no-cache flag is necessary due to the fact that files being changed are pulled from GitHub. If the no-cache flag is not used, the newest commits from the GitHub repository will not be pulled.

To push to Heroku, go to How to Upload Changes to Heroku.

### Running Docker Container Locally ###

When running the docker container locally for debugging, it’s connected to the same Elasticsearch and Maria instances as Heroku.

If you want to run the project on your local computer as opposed to on Heroku, use this command **after stopping the container running on Heroku**:

```
docker run --env DB_HOST --env DB_NAME --env DB_PASS --env DB_USER --env ELASTIC_URL --env GITHUB_KEY --env KIBANA_URL --env SLACK_KEY test_dockerfile
```
If you want to run the container locally, but use local files for testing purposes, you can use a command like this:

```
docker run -v $(pwd)/credentials.cfg:/override.cfg && \
-v $(pwd)/infra.cfg:/infra.cfg -v $(pwd)/dashboard.cfg:/dashboard.cfg && \
-v $(pwd)/logs:/logs -v $(pwd)/identities.yaml:/identities.yaml && \
-v $(pwd)/projects.json:/projects.json  && \
-v $(pwd)/aliases.json:/aliases.json grimoirelab/installed
```

The above command can be extremely useful for debugging purposes, as you have access to the logs from SirMordred. You can also test any changes you have made to configuration files locally before pushing them to GitHub. Although the container in this command is *grimoirelab/installed* as opposed to the *test_dockerfile* image used for the Heroku app, it essentially completes the same job, with the exception of not running the extra scripts that I have written.

## Additional Scripts ##
### manage-dashboards.py ###
### set_config.py ###
### get_projects.py ###
### create_dashboard.py ###
### enrich_identities.py ###
### create_identities.py ###
### entrypoint.sh ###
## Heroku ##
### Add-Ons (MariaDB and Elasticsearch) ###
#### Elasticsearch and Kibana ####
### Potential Problems with Database ###
### Reset Container Running on Heroku ###
### Nginx ###
## What Runs Where ##

# How to Update Code #
## Change in Credentials ##
## Adding a New Section to Kibana ##
### Files to be Changed ###
### How to Upload Changes to Heroku ###
### Additional Information ###

# Useful Tools #

# Potential Next Steps #
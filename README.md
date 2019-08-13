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

**Please note: if the changes you are making include adding a new section to Kibana, please go to [Adding a New Section to Kibana](https://github.com/openedx/metrics-dashboard#adding-a-new-section-to-kibana) before rebuilding the image.**

To rebuild the Dockerfile, use the command in the project directory:

```
docker build --tag=test_dockerfile --no-cache .
```

The no-cache flag is necessary due to the fact that files being changed are pulled from GitHub. If the no-cache flag is not used, the newest commits from the GitHub repository will not be pulled.

To push to Heroku, go to [How to Upload Changes to Heroku](https://github.com/openedx/metrics-dashboard#how-to-upload-changes-to-heroku).

### Running Docker Container Locally ###

When running the docker container locally for debugging, it’s connected to the same Elasticsearch and Maria instances as Heroku.

If you want to run the project on your local computer as opposed to on Heroku, use this command **after stopping the container running on Heroku**:

```
docker run --env DB_HOST --env DB_NAME --env DB_PASS && \
--env DB_USER --env ELASTIC_URL --env GITHUB_KEY && \
--env KIBANA_URL --env SLACK_KEY test_dockerfile
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
Used to import and export Kibana dashboards. 

To export dashboards (i.e. save dashboards from Kibana to local computer), run this command locally:

```python3 manage-dashboards.py export```

To import dashboards (i.e. load dashboards into Kibana from local computer), run this command locally:

```python3 manage-dashboards.py import```

Dashboards will be automatically exported to and imported from the dashboards directory that can be found in your local clone of the metrics dashboard GitHub repository. 

This script will only save dashboards locally. To save dashboards to the GitHub, push them to the repository. 
### set_config.py ###
Used to configure SirMordred with sensitive information that cannot be hard-coded. Program reads environment variables and then writes their values to infra.cfg, a configuration file used by SirMordred.
### get_projects.py ###
Used to modify the projects.json file, which specifies which repositories and Slack channels to pull from. The program gathers all public repositories in a given organization and all non-archived Slack channels readable by the given Slack api-token. 
### create_dashboard.py ###
Orchestrates getting the credentials for API access and retrieving all repository and Slack channel for a given organization or repository. 
### enrich_identities.py ###
Scrapes information from all Git commits in repositories in the edX organization. Program is used to update emails for individuals to aid in the use of SortingHat, which assigns individuals to an organization and maps data (Slack messages, Git commits) to an individual.
### create_identities.py ###
Parses .yaml file in edX format (people.yaml) and converts it to a format that is parsable by GrimoireLabs.
### entrypoint.sh ###
Script run in docker container when docker run command is issued. Runs many of the scripts listed above to set up config files before starting SirMordred.
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
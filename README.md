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
### Running Docker Container Locally ###
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
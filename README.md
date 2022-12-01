# metrics-dashboard #

![status](https://img.shields.io/badge/status-deprecated-AB0D02)

**OBSOLETE AND DEPRECATED**

This repository has been accepted as deprecated per the [Open edX DEPR
process](https://open-edx-proposals.readthedocs.io/en/latest/processes/oep-0021-proc-deprecation.html). It
has been moved to openedx-unsupported for historical purposes.

---

Dashboard for Open edX intended to run in a docker container.

Link for admin access (must enter username and password): https://66f663f015aecb785655faf0aae52d04.us-east-1.aws.found.io:9243

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

Should changes be made to the Dockerfile itself or to files in the GitHub repository, those files will need to be pushed to GitHub, and the Dockerfile will need to be rebuilt and pushed to Heroku.

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
Heroku integrates seamlessly with Docker to allow a user to push containers to a Heroku app. The process/container that runs SirMordred is hosted in a worker dyno on the openedx-metrics Heroku app. To check the logs of the openedx-metrics app use the command:

```heroku logs -a openedx-metrics --tail```

It is also good to note that when looking at the logs you will see errors that look like this:

Max retries error for GitHub
![GitHub Error Message](https://github.com/openedx/metrics-dashboard/blob/master/images/github_error.png?s=200)

Fetch members failed error for Slack
![Slack Error Message](https://github.com/openedx/metrics-dashboard/blob/master/images/slack_error.png?s=200)

These errors are normal, so do not worry! The program will continue to run as expected.

### Add-Ons (MariaDB and Elasticsearch) ###
There are two Heroku add-ons for the metrics dashboard project. One is a MariaDB add-on, while the other is an Elasticsearch add-on. Although the metrics dashboard project itself is hosted on Heroku, both of these add-ons are hosted on AWS and maintained by third parties. If any issues with the metrics dashboard should arise, checking the status of the add-ons is a good place to start after checking the logs of the app. To check the status of the apps, you can visit the individual settings pages by going to the [resources tab](https://dashboard.heroku.com/apps/openedx-metrics/resources) of the Heroku app, and then clicking on each of the add-on links.
#### Elasticsearch and Kibana ####
You can use the Kibana UI to directly edit and save dashboards. If you want to also save the dashboards locally and then push them to GitHub, use [manage-dashboards.py](https://github.com/openedx/metrics-dashboard#manage-dashboardspy).

Using the Kibana UI, you can also add new users and grant them permissions. To do this, go to the Management tab on Kibana, and click “Users”. There are several predefined roles, which are outlined on the [Elasticsearch website](https://www.elastic.co/guide/en/elastic-stack-overview/current/built-in-roles.html).
### Potential Problems with Database ###
If the database runs out of space, data from our sources will no longer be loaded correctly. If this is a problem, you will find an error in the Heroku logs that says “command INSERT denied to user . . .”. The current storage capacity is 1GB, and it should last us a while.
### Reset Container Running on Heroku ###
If you find it necessary to reset the Docker container running on Heroku, issue the command:

```heroku ps:restart worker -a openedx-metrics```

### Nginx ###
In the web dyno of the Heroku app, there is an nginx reverse proxy server running in a docker container. The purpose of the server is to allow anonymous access to the dashboard and also allow users to use a short url (https://openedx-metrics.herokuapp.com) instead of the url for the AWS instance that Kibana is running on. You cannot log into your admin account if you use the short url due to how the reverse proxy server is set up.

To build nginx container and push to Heroku, use these commands while in the nginx directory:

```
docker build -t web .
heroku container:push web --app openedx-metrics
heroku container:release web --app openedx-metrics
```

## What Runs Where ##

![Heroku App Layout](https://github.com/openedx/metrics-dashboard/blob/master/images/Heroku_App_Layout.png?s=200)

The above photo shows the configuration of the project while it is running on Heroku. Elasticsearch and MariaDB are both Heroku add-ons, meaning that they are managed by third parties. The docker container used for the metrics dashboard app is run by a Heroku worker dyno, and has access to the add-ons through the add-ons’ URLs. The web dyno on Heroku contains a docker container running a reverse proxy nginx server. The web dyno has access to the accessible port on the Heroku app.

# How to Update Code #
## Change in Credentials ##
If any database, Elasticsearch, or API-token credentials are changed, environment variables on the Heroku app [settings page](https://dashboard.heroku.com/apps/openedx-metrics/settings) and on your local computer (for local testing purposes) should be updated to reflect those credential changes. The containers on Heroku will restart automatically if any environment variables on Heroku are changed.

## Adding a New Section to Kibana ##
A potential next step in the project would be to add a panel to analyze the Open edX discourse activity. Several steps must be taken in order to successfully add the panel, which are detailed below. **Please save current dashboards and push to GitHub before making changes.**
### Files to be Changed ###
In order to add a new data source to pull from (i.e. Discourse, mailing list, etc.) two files need to be changed. The first file to be changed, dashboard.cfg, contains non-sensitive information necessary for SirMordred such as index names, default information for panels, and phases of SirMordred to complete. If you want to add a new data source, you must add something similar to the following to the dashboard.cfg file:

```
[discourse]
raw_index = discourse_grimoirelab-raw
enriched_index = discourse_grimoirelab
```

Details of what is needed in the section will be in the Perceval documentation for the data source.

Under the [phases] section of dashboard.cfg, you must also change panels to true, to ensure that the new indices for your section will be added.

The other file that must be changed is projects.json, which outlines all URLs to collect data from. To add another data source, simply add another key in the dictionary specified by the value of “Open edX” similar to the current layout of the “git” or “slack” keys.

### How to Upload Changes to Heroku ###
Once the necessary files have been changed, **and the current dashboards have been saved**, you can run the docker build command mentioned in [Building Dockerfile](https://github.com/openedx/metrics-dashboard#building-dockerfile).

Then run these series of commands:

```
heroku login
heroku container:login
docker tag test_dockerfile registry.heroku.com/openedx-metrics/worker
docker push registry.heroku.com/openedx-metrics/worker
heroku container:release worker -a openedx-metrics
```

After running the commands, make sure to import the previous dashboards you had saved using [manage-dashboards.py](https://github.com/openedx/metrics-dashboard#building-dockerfile)'s import functionality, so that you can keep any changes you made to the dashboards previous to releasing the application.

### Restore Dashboard Settings ###
After letting the new configuration settings run for a day, we now need to reset some of the changes in dashboard.cfg to prevent the container from rewriting panels every time it is started. In order to do this, under the [phases] section of dashboard.cfg, we want to change panels back to false. Push these changes to Github, rebuild the container, and push to Heroku again (the same steps outlined in the section above).


### Additional Information ###
While you may think that adding a new section is straight forward, you may run into various unexpected requirements for how new sections should be added into the projects.json file. For example, when adding a new Slack section, the channels must be listed by their channel identifier alone, not in a URL, while the Git and Github sections both require URLs. The repository for [Perceval](https://github.com/chaoss/grimoirelab-perceval) has some information on how to format new sources of data, should you need it.

# Useful Tools #
* To check the status of indices in Elastic search, you can use:
```
curl https://<username>:<password>@847c0596a6326412c0313eb32d88595a.us-east-1.aws.found.io:9243/_cat/indices
```

* If you find the need to check the contents of the database, you can use [DBeaver](https://dbeaver.io/) and connect remotely to the database.

# Potential Next Steps #
A good next step for the project would be to add in data from Discourse.

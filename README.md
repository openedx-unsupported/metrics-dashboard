# metrics-dashboard
Dashboard for Open edX intended to run in a docker container. 

Link for admin access (must enter username and password):https://66f663f015aecb785655faf0aae52d04.us-east-1.aws.found.io:9243

Link for read only access (anonymous access): https://openedx-metrics.herokuapp.com

# Components
## GrimoireLab
Created by [Bitergia](https://bitergia.com/about/), GrimoireLab is open source software that can be used for data analytics. The specific software used in the metrics dashboard project is comprised of several parts, which are outlined in the [GrimoireLab tutorial](https://chaoss.github.io/grimoirelab-tutorial/README.html).

### Configuration Files for GrimoireLab
## Docker
### Building Dockerfile
### Running Docker Container Locally
## Additional Scripts
### manage-dashboards.py
### set_config.py
### get_projects.py
### create_dashboard.py
### enrich_identities.py
### create_identities.py
### entrypoint.sh
## Heroku
### Add-Ons (MariaDB and Elasticsearch)
#### Elasticsearch and Kibana
### Potential Problems with Database
### Reset Container Running on Heroku
### Nginx
## What Runs Where

# How to Update Code
## Change in Credentials
## Adding a New Section to Kibana
### Files to be Changed
### How to Upload Changes to Heroku
### Additional Information

# Useful Tools

# Potential Next Steps
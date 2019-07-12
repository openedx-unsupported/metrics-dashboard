#!/bin/bash

cd /

sudo /usr/bin/python3 /set_config.py $GITHUB_KEY $SLACK_KEY $DB_USER $DB_PASS $DB_HOST $DB_NAME $ELASTIC_URL $KIBANA_URL
/usr/bin/python3 /create_dashboard.py -r /og_projects.json -wr /projects.json -cf /override.cfg

#sleep 5
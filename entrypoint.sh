#!/bin/bash

echo "Starting GrimoireLabs. . . "
cd /
echo "Configuring credentials . . ."
/usr/bin/python3 /set_config.py $GITHUB_KEY $SLACK_KEY $DB_USER $DB_PASS $DB_HOST $DB_NAME $ELASTIC_URL $KIBANA_URL
echo "Loading projects . . . "
/usr/bin/python3 /create_dashboard.py -r /og_projects.json -wr /projects.json -cf /override.cfg
sleep 5

git clone https://$GITHUB_KEY@github.com/edx/repo-tools-data.git
cp repo-tools-data/people.yaml .
rm -rf repo-tools-data
echo "Loading identities . . . "
/usr/bin/python3 /create_identities.py

sleep 5

/usr/local/bin/sirmordred -c /infra.cfg /dashboard.cfg /project.cfg /override.cfg
echo "sirmordred started!!! :)"

/usr/bin/python3 manage-dashboards.py import
echo "dashboard imported!"

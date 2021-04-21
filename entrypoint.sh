#!/bin/bash

echo "Starting GrimoireLabs. . . "
cd /
echo "Configuring credentials . . ."
python3.9 /set_config.py $GITHUB_KEY $SLACK_KEY $DB_USER $DB_PASS $DB_HOST $DB_NAME $ELASTIC_URL $KIBANA_URL $DISCOURSE_KEY

echo "Loading projects . . . "
python3.9 /create_dashboard.py -r /og_projects.json -wr /projects.json -cf /override.cfg
sleep 5

echo "projects.json is . . . "
cat /projects.json

git clone https://$GITHUB_KEY@github.com/edx/repo-tools-data.git
cp repo-tools-data/people.yaml .
rm -rf repo-tools-data
echo "Loading identities . . . "
python3.9 /create_identities.py

sleep 5

echo "Starting SirMordred"

/usr/local/bin/sirmordred -c /infra.cfg /dashboard.cfg /project.cfg /override.cfg

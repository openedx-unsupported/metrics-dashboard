"""
Used to gather the slack and github api tokens from an environment variable,
and then write those to a config file. 
"""

import os
import configparser

def get_tokens():
	github = os.environ['GITHUB_KEY']
	slack = os.environ['SLACK_KEY']
	db_user = os.environ['DB_USER']
	db_pass = os.environ['DB_PASS']
	elastic_url = os.environ['ELASTIC_URL']
	kibana_url = os.environ['KIBANA_URL']

	return {
			"github": github, 
			"slack": slack,
			"db_user": db_user,
			"db_pass": db_pass,
			"elastic_url": elastic_url,
			"kibana_url": kibana_url
			}

def write_config(tokens):
	infra_config = configparser.RawConfigParser()

	infra_config.read('infra.cfg')
	infra_config.set('es_collection', 'url', tokens['elastic_url'])
	infra_config.set('es_enrichment', 'url', tokens['elastic_url'])
	infra_config.set('sortinghat', 'user', tokens['db_user'])
	infra_config.set('sortinghat', 'password', tokens['db_pass'])
	infra_config.set('panels', 'kibiter_url', tokens['kibana_url'])

	with open('infra.cfg', 'w') as configfile:
		infra_config.write(configfile)

	token_config = configparser.RawConfigParser()

	token_config.add_section('github')
	token_config.set('github', 'api-token', tokens['github'])
	token_config.add_section('slack')
	token_config.set('slack', 'api-token', tokens['slack'])

	with open('override.cfg', 'w') as configfile:
		token_config.write(configfile)

if __name__ == '__main__':
	tokens = get_tokens()
	write_config(tokens)
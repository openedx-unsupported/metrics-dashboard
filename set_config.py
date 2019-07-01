"""
Used to gather the slack and github api tokens from an environment variable,
and then write those to a config file. 
"""

import os
import configparser

def get_tokens():
	github = os.environ['GITHUB_KEY']
	slack = os.environ['SLACK_KEY']

	return {"github": github, "slack": slack}

def write_config(tokens):
	config = configparser.RawConfigParser()
	config.add_section('github')
	config.set('github', 'api-token', tokens['github'])
	config.add_section('slack')
	config.set('slack', 'api-token', tokens['slack'])

	with open('override.cfg', 'w') as configfile:
		config.write(configfile)

if __name__ == '__main__':
	tokens = get_tokens()
	write_config(tokens)
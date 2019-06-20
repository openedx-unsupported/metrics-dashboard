"""
Used to create a projects.json file based on a json file that specifies only an org name (see
more in get_projects.py) and then call sirmordred.
"""
import json
import get_projects
import os
import configparser

def read_og_projects(filename):
	projects = {}
	with open(filename) as json_file:
		projects = json.load(json_file)
	return projects

def write_projects(projects):
	with open('projects.json', 'w+') as outfile:
		json.dump(projects, outfile)

def initialize():
	if os.path.exists('projects.json'):
		os.remove('projects.json')

def get_config(filename):
	#get api-tokens for github and slack
	config = configparser.ConfigParser()
	config.read(filename)
	return config


if __name__ == '__main__':
	initialize()
	projects = read_og_projects('og_projects.json')
	config = get_config('credentials.cfg')
	new_projects = get_projects.create_projects(projects, config)
	write_projects(new_projects)
